from pathlib import Path


def read_binary_file(path):
    """Return all bytes from a binary file."""
    raise NotImplementedError


def read_binary_header(path, size=8):
    """Return up to size bytes from the beginning of a binary file."""
    raise NotImplementedError


def validate_nonempty_file(path):
    """Return a Path for a valid, existing, non-empty file.

    Raise:
        FileNotFoundError: if the path does not exist.
        ValueError: if the path is not a regular file or is empty.
    """
    raise NotImplementedError


def validate_score(value):
    """Convert value to float and return it if it is between 0 and 100.

    Raise:
        ValueError: if value is not numeric or is outside 0..100.
    """
    raise NotImplementedError


def parse_record(line):
    """Parse 'student_id,name,score' into a validated record dictionary.

    Leading/trailing whitespace around each field should be ignored.

    Raise:
        ValueError: if the record does not contain exactly three fields,
                    student_id or name is blank, or score is invalid.
    """
    raise NotImplementedError


def import_records(path):
    """Import valid student records from a UTF-8 text file.

    Each nonblank line is expected to contain:
        student_id,name,score

    Invalid lines should be skipped rather than terminating the import.

    Return:
        tuple: (valid_records, errors)

    valid_records is a list of record dictionaries.
    errors is a list of dictionaries with:
        line_number, line, error
    """
    raise NotImplementedError


def save_rejected_records(path, errors):
    """Write rejected-record information to a UTF-8 text file.

    Create the parent folder if needed and return the Path written.
    """
    raise NotImplementedError


def import_summary(records, errors):
    """Return a summary dictionary for the import results.

    Expected keys:
        imported
        rejected
        average_score
        names
    """
    raise NotImplementedError
