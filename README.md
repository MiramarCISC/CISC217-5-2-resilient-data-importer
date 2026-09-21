# CISC 217 Week 5 — Resilient Data Importer

## Topic
Binary files, exceptions, and validation.

## Goal
Complete `src/cisc217_week5/resilient_importer.py`.

Your program will read binary data, validate files and scores, parse student records, continue when individual records are invalid, preserve useful error information, and summarize the import.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[test]
python -m pytest -q
```

## Required Functions
- `read_binary_file()`
- `read_binary_header()`
- `validate_nonempty_file()`
- `validate_score()`
- `parse_record()`
- `import_records()`
- `save_rejected_records()`
- `import_summary()`

Read the docstrings and tests for exact expected behavior.

## Rules
- Use `pathlib.Path`.
- Use binary mode for binary data.
- Use UTF-8 for text files.
- Catch only exceptions you expect.
- Invalid individual records must not terminate the entire import.
- Do not silently discard invalid records; preserve useful error information.
- Do not modify the tests to make your code pass.

## Submit
1. Run `python -m pytest -q`.
2. Commit your work.
3. Push to `main`.
4. Confirm the Classroom50 autograder passes.
5. Post your repository link and lab evidence in Canvas.
