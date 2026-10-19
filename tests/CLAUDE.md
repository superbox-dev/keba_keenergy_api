# Tests

- Setters: also test invalid input
- Large expected values (e.g. `read_data()` results, multi-request payloads) as syrupy snapshots, small values inline
  - always review the `__snapshots__/*.ambr` diff
- Never call, patch or inspect `_`-prefixed methods or attributes, assert return values, exceptions or the sent payload
- `pytest.mark.parametrize` with `ids=` naming each case
