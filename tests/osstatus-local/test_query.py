"""Behavior checks against the actual imported OSStatus snapshot."""

import importlib.util
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2] / "skills"
SCRIPT = ROOT / "osstatus-local" / "scripts" / "osstatus.py"
spec = importlib.util.spec_from_file_location("osstatus_query", SCRIPT)
query = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query)


class CatalogSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = query.connect(query.DEFAULT_DB)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def search(self, value="", **filters):
        return query.search(self.connection, value, limit=None, **filters)

    def ids(self, value):
        return {row["id"] for row in self.search(value)["results"]}

    def test_negative_code_is_exact_and_preserves_framework_collisions(self):
        result = self.search("-50")
        symbols = {row["symbol"] for row in result["results"]}
        self.assertTrue({"paramErr", "errSecParam", "AVAudioSessionErrorCodeBadParam"} <= symbols)
        for row in result["results"]:
            self.assertTrue({-50, 4294967246} & {code["integer_value"] for code in row["codes"]})

    def test_signed_unsigned_and_hex_return_same_records(self):
        self.assertEqual(self.ids("-50"), self.ids("4294967246"))
        self.assertEqual(self.ids("-50"), self.ids("0xFFFFFFCE"))

    def test_fourcc_and_decimal_return_same_records(self):
        ids = self.ids("'fmt?'")
        self.assertTrue(ids)
        self.assertEqual(ids, self.ids("1718449215"))
        self.assertEqual(ids, self.ids("0x666d743f"))
        self.assertEqual(ids, self.ids("fmt?"))
        self.assertIn("kAudioFormatUnsupportedDataFormatError", {
            row["symbol"] for row in self.search("'fmt?'")["results"]})

    def test_larger_than_uint32_source_value_is_not_wrapped(self):
        rows = self.search("4294967644")["results"]
        self.assertTrue(rows)
        self.assertIn("MACH_SEND_INVALID_RT_OOL_SIZE", {row["symbol"] for row in rows})
        self.assertTrue(self.ids("4294967644").isdisjoint(self.ids("348")))

    def test_fourcc_trailing_space_is_preserved(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "run ", "--all", "--json"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        expected = self.ids("1920298528")
        self.assertTrue(expected)
        self.assertEqual({row["id"] for row in payload["results"]}, expected)
        self.assertEqual(self.ids("'run '"), expected)

    def test_source_anomalies_are_visible_without_changing_values(self):
        result = self.search("MACH_SEND_INVALID_RT_OOL_SIZE")
        row = result["results"][0]
        self.assertTrue(row["warnings"])
        self.assertIn("0x10000015compatibility: no longer a returned error", [code["text"] for code in row["codes"]])
        self.assertIn(4294967644, [code["integer_value"] for code in row["codes"]])
        output = io.StringIO()
        with redirect_stdout(output):
            query.print_results(result)
        self.assertIn("Source warning:", output.getvalue())

    def test_duplicate_symbol_records_are_retained(self):
        rows = self.search("AVAudioSessionErrorCodeBadParam")["results"]
        self.assertTrue({"AVFAudio", "CoreAudioTypes"} <= {row["framework"] for row in rows})

    def test_symbol_and_filters_find_specific_record(self):
        result = self.search("errSecAuthFailed", framework="security", header="SecBase", platform="visionOS")
        self.assertEqual(result["total"], 1)
        row = result["results"][0]
        self.assertEqual(row["symbol"], "errSecAuthFailed")
        self.assertIn(-25293, [code["integer_value"] for code in row["codes"]])
        self.assertEqual(row["description"], "")
        self.assertTrue(row["source_url"].startswith("https://www.osstatus.com/"))

    def test_description_search_decodes_entities(self):
        result = self.search("current protection policy")
        row = next(row for row in result["results"] if row["symbol"] == "ACErrorAccessDeniedByProtectionPolicy")
        self.assertIn("couldn't fetch a credential", row["description"])

    def test_multiword_query_matches_across_fields(self):
        rows = self.search("security SecBase.h", platform="macOS")["results"]
        self.assertTrue(rows)
        self.assertTrue(all(row["framework"] == "Security" and row["header"] == "SecBase.h" for row in rows))

    def test_limit_reports_unshown_results(self):
        result = query.search(self.connection, "", limit=3)
        self.assertEqual(result["shown"], 3)
        self.assertGreater(result["total"], 6000)
        self.assertTrue(result["truncated"])

    def test_absent_and_sql_metacharacter_queries_are_literal(self):
        self.assertEqual(self.search("__osstatus_unknown_abcdef__")["total"], 0)
        self.assertEqual(self.search("%' OR 1=1 --")["total"], 0)
        self.assertEqual(self.search(str(1 << 100))["total"], 0)

    def test_database_is_opened_read_only(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.connection.execute("CREATE TABLE accidental_write (id INTEGER)")

    def test_cli_json_and_exit_codes(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "-50", "--framework", "Security", "--json"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("errSecParam", {row["symbol"] for row in payload["results"]})
        absent = subprocess.run([sys.executable, str(SCRIPT), "__osstatus_unknown_abcdef__", "--json"], text=True, capture_output=True)
        self.assertEqual(absent.returncode, 1)
        self.assertEqual(json.loads(absent.stdout)["total"], 0)
        invalid = subprocess.run([sys.executable, str(SCRIPT), "--limit", "0"], text=True, capture_output=True)
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("must be positive", invalid.stderr)

    def test_cli_works_with_socket_creation_blocked(self):
        output = io.StringIO()
        with mock.patch("socket.socket", side_effect=AssertionError("Network access attempted")), redirect_stdout(output):
            status = query.main(["-25293", "--framework", "Security", "--json"])
        self.assertEqual(status, 0)
        self.assertIn("errSecAuthFailed", {row["symbol"] for row in json.loads(output.getvalue())["results"]})

    def test_compact_and_full_json_preserve_lookup_results(self):
        cases = [
            ["-25300", "--framework", "Security"],
            ["MACH_SEND_INVALID_RT_OOL_SIZE"],
            [],
        ]
        for arguments in cases:
            with self.subTest(arguments=arguments):
                compact_process = subprocess.run([sys.executable, str(SCRIPT), *arguments, "--json"], text=True, capture_output=True)
                full_process = subprocess.run([sys.executable, str(SCRIPT), *arguments, "--full-json"], text=True, capture_output=True)
                self.assertEqual(compact_process.returncode, 0, compact_process.stderr)
                self.assertEqual(full_process.returncode, 0, full_process.stderr)
                compact = json.loads(compact_process.stdout)
                full = json.loads(full_process.stdout)
                for key in ("query", "filters", "total", "shown", "truncated"):
                    self.assertEqual(compact[key], full[key])
                self.assertEqual(compact["shown"], len(compact["results"]))
                for small_row, full_row in zip(compact["results"], full["results"]):
                    self.assertNotIn("raw_fields", small_row)
                    self.assertEqual(full_row["raw_fields"]["value-symbol"], [full_row["symbol"]])
                    self.assertEqual(small_row, {key: value for key, value in full_row.items() if key != "raw_fields"})
                self.assertEqual(set(compact["metadata"]), {"source_name", "source_url", "source_updated", "retrieved_at", "schema_version"})
                self.assertTrue(compact["metadata"].items() <= full["metadata"].items())
                self.assertIn("source_sha256", full["metadata"])
                self.assertLess(len(compact_process.stdout), len(full_process.stdout))
                if arguments == ["MACH_SEND_INVALID_RT_OOL_SIZE"]:
                    self.assertTrue(compact["results"][0]["warnings"])
                if not arguments:
                    self.assertTrue(compact["truncated"])
                    self.assertEqual(compact["shown"], 20)

    def test_compacting_does_not_remove_full_programmatic_data(self):
        full = self.search("errSecItemNotFound")
        before = json.dumps(full, sort_keys=True)
        query.compact_json(full)
        self.assertEqual(json.dumps(full, sort_keys=True), before)
        self.assertIn("raw_fields", full["results"][0])
        self.assertIn("source_sha256", full["metadata"])

    def test_json_discovery_modes_keep_counts_and_full_provenance_option(self):
        for mode in ("--stats", "--frameworks"):
            with self.subTest(mode=mode):
                compact = json.loads(subprocess.check_output([sys.executable, str(SCRIPT), mode, "--json"], text=True))
                full = json.loads(subprocess.check_output([sys.executable, str(SCRIPT), mode, "--full-json"], text=True))
                self.assertEqual({key: value for key, value in compact.items() if key != "metadata"},
                                 {key: value for key, value in full.items() if key != "metadata"})
                self.assertNotIn("source_sha256", compact["metadata"])
                self.assertIn("source_sha256", full["metadata"])


if __name__ == "__main__":
    unittest.main()
