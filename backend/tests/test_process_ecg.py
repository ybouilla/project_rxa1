# test_ecg.py

import csv
import numpy as np
import pandas as pd
import pytest

from backend.process_ecg import (
    load_ecg_file,
    compute_heart_cycle_duration,
    compute_mean_heart_rate,
    compute_max_heart_rate,
    compute_min_heart_rate,
    process_ecg,
)

class TestEcgProcessing:

    @pytest.fixture
    def sample_ecg_file(self, tmp_path):
        file_path = tmp_path / "ecg.csv"

        rows = [
            ["QRS", "100", "120", "tag1"],
            ["P", "150", "170"],
            ["QRS", "1100", "1120", "tag2"],
            ["QRS", "2100", "2120"],
        ]

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return str(file_path)

    @pytest.fixture
    def qrs_dataframe(self):
        return pd.DataFrame(
            {
                "wave_type": ["QRS", "QRS", "QRS"],
                "wave_onset": ["100", "1100", "2100"],
                "wave_offset": ["120", "1120", "2120"],
                "wave_tags": ["a", "b", "c"],
            }
        )

    def test_load_ecg_file(self, sample_ecg_file):
        df = load_ecg_file(sample_ecg_file)

        assert len(df) == 4
        assert list(df.columns) == [
            "wave_type",
            "wave_onset",
            "wave_offset",
            "wave_tags",
        ]
        assert df.loc[0, "wave_type"] == "QRS"
        assert df.loc[0, "wave_tags"] == "tag1"
        assert df.loc[1, "wave_tags"] is None

    def test_load_empty_file(self, tmp_path):
        file_path = tmp_path / "empty.csv"
        file_path.write_text("")

        df = load_ecg_file(str(file_path))

        assert df.empty

    def test_compute_heart_cycle_duration(self, qrs_dataframe):
        cycles, df = compute_heart_cycle_duration(qrs_dataframe)

        np.testing.assert_array_equal(
            cycles,
            np.array([1000.0, 1000.0]),
        )

        assert "QRS_peek" in df.columns

    def test_compute_heart_cycle_duration_single_qrs(self):
        df = pd.DataFrame(
            {
                "wave_type": ["QRS"],
                "wave_onset": ["100"],
                "wave_offset": ["120"],
                "wave_tags": [None],
            }
        )

        cycles, _ = compute_heart_cycle_duration(df)

        assert len(cycles) == 0

    def test_compute_mean_heart_rate(self):
        cycles = np.array([1000.0, 1000.0])

        bpm = compute_mean_heart_rate(cycles)

        assert bpm == 60.0

    def test_compute_max_heart_rate(self):
        cycles = np.array([1000.0, 800.0])

        df = pd.DataFrame(
            {
                "wave_onset": [100, 1100, 1900],
            }
        )

        bpm, start, end = compute_max_heart_rate(cycles, df)

        assert bpm == 75.0
        assert start == 1100.0
        assert end == 1900.0

    def test_compute_min_heart_rate(self):
        cycles = np.array([1000.0, 1200.0])

        df = pd.DataFrame(
            {
                "wave_onset": [100, 1100, 2300],
            }
        )

        bpm, start, end = compute_min_heart_rate(cycles, df)

        assert bpm == 50.0
        assert start == 1100.0
        assert end == 2300.0

    @pytest.mark.parametrize(
        "cycle, expected_bpm",
        [
            (1000.0, 60.0),
            (800.0, 75.0),
            (1200.0, 50.0),
        ],
    )
    def test_bpm_conversion(self, cycle, expected_bpm):
        bpm = compute_mean_heart_rate(np.array([cycle]))

        assert bpm == expected_bpm

    def test_process_ecg(self, sample_ecg_file):
        result = process_ecg(sample_ecg_file)

        mean_hr, min_hr, max_hr = result

        assert mean_hr == 60.0
        assert min_hr[0] == 60.0
        assert max_hr[0] == 60.0
        assert len(result) == 3