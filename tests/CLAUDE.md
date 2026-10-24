# Tests

- Setters: also test invalid input
- Large expected values (e.g. `read_data()` results, multi-request payloads) as syrupy snapshots, small values inline
  - always review the `__snapshots__/*.ambr` diff
- Never call, patch or inspect `_`-prefixed methods or attributes, assert return values, exceptions or the sent payload
- `pytest.mark.parametrize` with `ids=` naming each case
- Constants of a test module in a module with its name and `_data.py` (`test_api.py` → `test_api_data.py`)
  - shared by several test modules: `tests/conftest.py`
- Helper functions that only check (no return value) start with `assert_`
  - helpers that return a value and only assert to narrow types keep their name
  - shared by several test modules: `tests/asserts.py`, registered with `pytest.register_assert_rewrite()` in
    `tests/conftest.py`
- Tests as functions, no test classes
- Error cases next to the tests of the code they check, named `test_<function>_<condition>`
- Coverage stays at 100 %, every new code path needs a test
- Every bug fix gets a regression test that fails without the fix
- Exceptions: assert the type and the message (`pytest.raises(..., match=...)` or `error.value`)
- Never wait in real time, no `sleep()` with a delay, patch the time instead
- Fixtures only in `tests/conftest.py`
- Tests are independent of each other, they run in parallel (`pytest-xdist`) and in any order
- No logic in tests (`if`, loops over cases), use `parametrize` instead
  - except loops that only build test data
