# Static Analysis Issues

The line numbers below refer to the original version of `shuttle_system.py`
before the fixes.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Deleted route lookup | High - runtime bug | 55-58 | `R3` was deleted and then accessed again, causing a `KeyError`. Unknown user-entered routes also caused a `KeyError`. | Removed the stale `R3` average lookup and validate the selected route before indexing. |
| Broad exception handling | High - correctness | 26-31 | A bare `except` hid all failures, including invalid passenger data and empty trip lists. | Validate trip data, skip routes with no trips, and let unexpected errors remain visible. |
| Invalid passenger data | High - data validation | 49-50 | A negative count and the string `"full"` made averages invalid or caused a `TypeError`. | Require non-negative integer counts and use valid sample data. |
| Mutable default argument | Medium - reliability | 11 | `logs=[]` shared state between calls, so later calls could unexpectedly reuse earlier log entries. | Use `None` as the default and create a fresh list per call. |
| Unclosed file handles | Medium - resource management | 35-40 | Files were opened and closed manually, so an exception could leave handles open. | Use `with open(...)` context managers with explicit UTF-8 encoding. |
| Non-idiomatic function name | Low - maintainability | 40 | `assignDriver` did not follow Python naming conventions and reduced readability. | Rename it to `assign_driver`. |

