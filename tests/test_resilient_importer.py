from pathlib import Path

import pytest

from cisc217_week5.resilient_importer import (
    read_binary_file,
    read_binary_header,
    validate_nonempty_file,
    validate_score,
    parse_record,
    import_records,
    save_rejected_records,
    import_summary,
)


def test_read_binary_file_returns_bytes(tmp_path):
    path = tmp_path / "sample.bin"
    path.write_bytes(b"\x00\x01Python\xff")
    data = read_binary_file(path)
    assert isinstance(data, bytes)
    assert data == b"\x00\x01Python\xff"


def test_read_binary_header_limits_bytes(tmp_path):
    path = tmp_path / "sample.bin"
    path.write_bytes(b"ABCDEFGH1234")
    assert read_binary_header(path, 4) == b"ABCD"
    assert read_binary_header(path, 8) == b"ABCDEFGH"


def test_validate_nonempty_file_returns_path(tmp_path):
    path = tmp_path / "data.bin"
    path.write_bytes(b"\x01")
    result = validate_nonempty_file(path)
    assert isinstance(result, Path)
    assert result == path


def test_validate_nonempty_file_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_nonempty_file(tmp_path / "missing.bin")


def test_validate_nonempty_file_directory_raises(tmp_path):
    with pytest.raises(ValueError):
        validate_nonempty_file(tmp_path)


def test_validate_nonempty_file_empty_raises(tmp_path):
    path = tmp_path / "empty.bin"
    path.write_bytes(b"")
    with pytest.raises(ValueError):
        validate_nonempty_file(path)


@pytest.mark.parametrize(("value", "expected"), [(0, 0.0), ("88.5", 88.5), (100, 100.0)])
def test_validate_score_accepts_valid_values(value, expected):
    assert validate_score(value) == expected


@pytest.mark.parametrize("value", ["bad", None, -1, 100.1])
def test_validate_score_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        validate_score(value)


def test_parse_record_returns_validated_dictionary():
    assert parse_record(" s001 , Ada , 95 ") == {
        "student_id": "s001", "name": "Ada", "score": 95.0
    }


@pytest.mark.parametrize("line", [
    "s001,Ada", "s001,Ada,95,extra", ",Ada,95", "s001,,95", "s001,Ada,bad", "s001,Ada,150"
])
def test_parse_record_rejects_invalid_records(line):
    with pytest.raises(ValueError):
        parse_record(line)


def test_import_records_keeps_valid_rows_and_reports_errors(tmp_path):
    path = tmp_path / "records.txt"
    path.write_text(
        "s001,Ada,95\n"
        "\n"
        "s002,Grace,88.5\n"
        "s003,Missing Score,bad\n"
        ",No ID,77\n"
        "s004,Linus,91\n",
        encoding="utf-8",
    )
    records, errors = import_records(path)
    assert records == [
        {"student_id": "s001", "name": "Ada", "score": 95.0},
        {"student_id": "s002", "name": "Grace", "score": 88.5},
        {"student_id": "s004", "name": "Linus", "score": 91.0},
    ]
    assert len(errors) == 2
    assert errors[0]["line_number"] == 4
    assert errors[0]["line"] == "s003,Missing Score,bad"
    assert isinstance(errors[0]["error"], str)
    assert errors[1]["line_number"] == 5


def test_import_records_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        import_records(tmp_path / "missing.txt")


def test_save_rejected_records_creates_parent_and_writes(tmp_path):
    path = tmp_path / "output" / "rejected.txt"
    errors = [{"line_number": 3, "line": "s003,Ada,bad", "error": "score must be numeric"}]
    written = save_rejected_records(path, errors)
    assert written == path
    text = path.read_text(encoding="utf-8")
    assert "3" in text
    assert "s003,Ada,bad" in text
    assert "score must be numeric" in text


def test_import_summary_reports_counts_average_and_names():
    records = [
        {"student_id": "s002", "name": "Grace", "score": 88.5},
        {"student_id": "s001", "name": "Ada", "score": 95.0},
        {"student_id": "s003", "name": "Linus", "score": 91.0},
    ]
    errors = [{"line_number": 4, "line": "bad", "error": "invalid"}]
    assert import_summary(records, errors) == {
        "imported": 3, "rejected": 1, "average_score": 91.5, "names": ["Ada", "Grace", "Linus"]
    }


def test_import_summary_empty_records():
    assert import_summary([], []) == {
        "imported": 0, "rejected": 0, "average_score": 0.0, "names": []
    }
