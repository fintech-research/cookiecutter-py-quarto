from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from example_project.utils.files import (
    MissingFileParamError,
    get_latest_file,
    timestamp_file,
)


class TestGetLatestFile:
    """Test suite for get_latest_file function."""

    def test_get_latest_file_with_prefix(self, tmp_path):
        """Test finding the latest file using prefix."""
        # Create test files with timestamps
        (tmp_path / "data_UTC20231015_120000.parquet").touch()
        (tmp_path / "data_UTC20231016_120000.parquet").touch()
        (tmp_path / "data_UTC20231017_120000.parquet").touch()

        result = get_latest_file(prefix="data", directory=tmp_path)

        assert result is not None
        assert result.name == "data_UTC20231017_120000.parquet"

    def test_get_latest_file_with_file_path(self, tmp_path):
        """Test finding the latest file using a file path."""
        # Create test files
        (tmp_path / "output_UTC20231015_120000.csv").touch()
        (tmp_path / "output_UTC20231016_120000.csv").touch()

        file_path = tmp_path / "output.csv"
        result = get_latest_file(file=file_path)

        assert result is not None
        assert result.name == "output_UTC20231016_120000.csv"

    def test_get_latest_file_custom_extension(self, tmp_path):
        """Test finding files with custom extension."""
        (tmp_path / "log_UTC20231015_120000.txt").touch()
        (tmp_path / "log_UTC20231016_120000.txt").touch()

        result = get_latest_file(prefix="log", extension=".txt", directory=tmp_path)

        assert result is not None
        assert result.name == "log_UTC20231016_120000.txt"

    def test_get_latest_file_no_matches(self, tmp_path):
        """Test when no matching files are found."""
        result = get_latest_file(prefix="nonexistent", directory=tmp_path)

        assert result is None

    def test_get_latest_file_missing_params(self):
        """Test that MissingFileParamError is raised when both file and prefix are None."""
        with pytest.raises(MissingFileParamError) as exc_info:
            get_latest_file()

        assert "Either file or prefix must be provided" in str(exc_info.value)

    def test_get_latest_file_file_overrides_prefix(self, tmp_path):
        """Test that file parameter takes precedence over prefix."""
        (tmp_path / "test_UTC20231015_120000.parquet").touch()
        (tmp_path / "test_UTC20231016_120000.parquet").touch()
        (tmp_path / "other_UTC20231017_120000.parquet").touch()

        file_path = tmp_path / "test.parquet"
        result = get_latest_file(file=file_path, prefix="other")

        assert result is not None
        assert result.name == "test_UTC20231016_120000.parquet"

    def test_get_latest_file_lexicographic_ordering(self, tmp_path):
        """Test that files are ordered lexicographically by stem."""
        # Create files with different timestamps
        (tmp_path / "data_UTC20231001_120000.parquet").touch()
        (tmp_path / "data_UTC20231015_120000.parquet").touch()
        (tmp_path / "data_UTC20230901_120000.parquet").touch()

        result = get_latest_file(prefix="data", directory=tmp_path)

        assert result is not None
        # Lexicographically, "data_UTC20231015_120000" > "data_UTC20231001_120000" > "data_UTC20230901_120000"
        assert result.name == "data_UTC20231015_120000.parquet"

    def test_get_latest_file_mixed_files(self, tmp_path):
        """Test that only matching files are considered."""
        # Create files with correct pattern
        (tmp_path / "data_UTC20231015_120000.parquet").touch()
        (tmp_path / "data_UTC20231016_120000.parquet").touch()
        # Create files that don't match the pattern
        (tmp_path / "data.parquet").touch()
        (tmp_path / "data_20231017.parquet").touch()
        (tmp_path / "other_UTC20231018_120000.parquet").touch()

        result = get_latest_file(prefix="data", directory=tmp_path)

        assert result is not None
        assert result.name == "data_UTC20231016_120000.parquet"


class TestTimestampFile:
    """Test suite for timestamp_file function."""

    def test_timestamp_file_basic(self):
        """Test that timestamp_file adds a UTC timestamp to the filename."""
        file_path = Path("data.parquet")
        result = timestamp_file(file_path)

        # Check that the result has the expected pattern
        assert result.stem.startswith("data_UTC")
        assert result.suffix == ".parquet"
        assert "_UTC" in result.name

    def test_timestamp_file_with_directory(self):
        """Test that timestamp_file preserves the directory path."""
        file_path = Path("output/subfolder/data.csv")
        result = timestamp_file(file_path)

        assert result.parent == Path("output/subfolder")
        assert result.stem.startswith("data_UTC")
        assert result.suffix == ".csv"

    def test_timestamp_file_format(self):
        """Test that the timestamp format is correct (YYYYMMDD_HHMMSS)."""
        file_path = Path("test.txt")
        result = timestamp_file(file_path)

        # Extract timestamp part
        stem = result.stem
        timestamp_part = stem.replace("test_UTC", "")

        # Check format: should be YYYYMMDD_HHMMSS
        assert len(timestamp_part) == 15  # 8 digits + underscore + 6 digits
        assert timestamp_part[8] == "_"

        # Verify it's a valid timestamp
        try:
            datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
        except ValueError:
            pytest.fail(f"Timestamp format is invalid: {timestamp_part}")

    def test_timestamp_file_different_extensions(self):
        """Test timestamp_file with various file extensions."""
        test_cases = [
            ("data.parquet", ".parquet"),
            ("output.csv", ".csv"),
            ("log.txt", ".txt"),
            ("archive.tar.gz", ".gz"),
        ]

        for filename, expected_ext in test_cases:
            file_path = Path(filename)
            result = timestamp_file(file_path)
            assert result.suffix == expected_ext

    def test_timestamp_file_no_extension(self):
        """Test timestamp_file with a file that has no extension."""
        file_path = Path("README")
        result = timestamp_file(file_path)

        assert result.stem.startswith("README_UTC")
        assert result.suffix == ""

    def test_timestamp_file_uses_utc(self):
        """Test that timestamp_file uses UTC timezone."""
        file_path = Path("test.parquet")
        before = datetime.now(tz=UTC)
        result = timestamp_file(file_path)
        after = before + timedelta(seconds=1)  # small margin

        # Extract timestamp from filename
        stem = result.stem
        timestamp_str = stem.replace("test_UTC", "")
        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S").replace(
            tzinfo=UTC
        )

        # Verify the timestamp is between before and after (with small margin)
        assert (before - timedelta(seconds=1)) <= timestamp <= after

    def test_timestamp_file_uniqueness(self):
        """Test that consecutive calls produce different timestamps (if enough time passes)."""
        file_path = Path("data.parquet")
        result1 = timestamp_file(file_path)

        # Small delay to ensure different timestamp
        import time

        time.sleep(1.1)

        result2 = timestamp_file(file_path)

        # The timestamps should be different
        assert result1.name != result2.name
