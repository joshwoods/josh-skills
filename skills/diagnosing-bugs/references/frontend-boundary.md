# Frontend bugs: reproduce, then locate the mismatch

Use this when a visible UI failure might come from the request, backend data, or client handling. The task is to find the first supported mismatch in the data path, rather than assigning ownership from the screen alone.

## 1. Preserve a useful reproduction

- [ ] Record the route, action order, relevant build/configuration, account or permissions, input records, and starting client/cache state. Include browser/device, flags, or timing only where relevant. Distinguish a fresh load from navigation through an existing session.
- [ ] Capture the visible result and the request/response belonging to that interaction. Record the method, relevant parameters/body, response status/content type, payload, and timing; use request IDs when available. Confirm the response corresponds to the affected record and action, rather than an unrelated background call.
- [ ] If reproduction is intermittent, retain the failing data and ordering. Compare a failing session with a working one. Inspect console errors and available traces when a fresh reproduction is unavailable; do not clear all state before preserving the conditions that may explain the failure.

**Keep:** Steps + starting state + matching exchange + actual UI result. In shared evidence, omit credentials and unrelated personal data while preserving the fields and relationships needed to explain the failure.

## 2. Inspect the path in order

- [ ] **Request:** Did the client send the intended endpoint, record ID, filters, pagination, body, and authorization context? If no request was sent, check event handling, validation, routing, and whether cached/local data was used. A response can be correct for the request actually sent while wrong for the user's intended action.
- [ ] **Response:** Inspect the raw response before application mapping, identifying whether it came through a proxy, service worker, or cache. Compare both shape and meaning with the contract and expected record: missing versus null, types, units, dates/time zones, values, freshness, completeness, and error semantics. Successful HTTP status or schema validation alone does not establish correct data. Browser-visible data does not by itself identify the originating component.
- [ ] **Client handling:** Compare raw response → decoded value → normalization/mapping → cache/store → selected view state → rendered output. Check stale cache entries, response ordering, request-to-view identity, and formatting where relevant. If no response is available, investigate the network/error path rather than inventing a payload.

Use the first observed mismatch to choose the next investigation:

| Evidence | Next branch |
| --- | --- |
| Request differs from the intended action | Trace how the client constructed or selected the request. |
| Correct request, but response violates the contract or contains incorrect values | Trace the response producer and data source; check API/version mismatch, server serialization, upstream data, or an intermediary/cache. Do not assume the frontend produced the bad value. |
| Response is correct, but parsed/mapped/stored/selected data differs | Investigate decoding, transformations, cache identity, state updates, or stale completions at the first mismatch. |
| View state is correct, but output is wrong | Investigate rendering, formatting, layout, or event-to-view binding. |
| Unusual response is allowed by the contract | Investigate the client's assumption about supported data, such as an optional field or empty result. |
| Response violates the contract and the UI also fails to handle the error as required | Record the upstream violation and client error-handling defect separately. Both may need repair. |
| The contract or expected record is unclear | Resolve that premise; label ownership unresolved until evidence supports it. |

## 3. Run a discriminating experiment

- [ ] Replay the captured response through the real client handling path in an isolated fixture, preserving relevant state and ordering. Compare with a known-correct response under the same conditions. Keep other relevant variables fixed.
- [ ] If replay reproduces the failure, it shows that data and client handling can produce the symptom; it does not by itself assign fault. If replay does not fail, investigate missing context such as cache state, race/order, auth, or integration behavior. A fabricated malformed payload tests handling, not whether the backend actually emits that payload.

## 4. Verify at the boundary that failed

- [ ] Fix the demonstrated cause. Do not make every unexpected value silently become a default merely to hide a broken contract; determine the required fallback or error behavior.
- [ ] Validate each claimed defect independently. If extra client defenses are desirable but not required by the supported behavior, label them a robustness recommendation rather than an established second bug.
- [ ] Recheck the original interaction with the actual integration, the relevant captured-data regression, and contract-valid edge cases. If error handling changed, check the relevant malformed/error case too. A mocked response alone does not verify the end-to-end repair.

Return to the [main checklist](checklist.md) to record the outcome, clean up probes, and complete the remaining scope.
