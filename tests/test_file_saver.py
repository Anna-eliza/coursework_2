import json
import os
import pytest
from src.aeroplane import Aeroplane
from src.file_saver import JSONSaver


class TestJSONSaverAdd:
    def test_add_one_aeroplane(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplane(sample_aeroplanes[0])
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["callsign"] == "UAL1621"

    def test_add_multiple_aeroplanes(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 3

    def test_add_to_existing_file(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplane(sample_aeroplanes[0])
        saver.add_aeroplane(sample_aeroplanes[1])
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 2


class TestJSONSaverGet:
    def test_get_all(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        result = saver.get_aeroplanes({})
        assert len(result) == 3

    def test_get_by_country(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        result = saver.get_aeroplanes({"origin_country": "France"})
        assert len(result) == 1
        assert result[0]["callsign"] == "TVF22UT"

    def test_get_by_velocity_min(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        result = saver.get_aeroplanes({"velocity_min": 250})
        assert len(result) == 2
        callsigns = {item["callsign"] for item in result}
        assert callsigns == {"UAL1621", "AFL123"}

    def test_get_by_velocity_max(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        result = saver.get_aeroplanes({"velocity_max": 250})
        assert len(result) == 1
        assert result[0]["callsign"] == "TVF22UT"

    def test_get_by_altitude_range(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        result = saver.get_aeroplanes({"altitude_min": 10500, "altitude_max": 11500})
        # AFL123 (11000) попадает, UAL1621 (10203) и TVF22UT (11567) — нет
        assert len(result) == 1
        assert result[0]["callsign"] == "AFL123"

    def test_get_empty_file(self, temp_json_file):
        saver = JSONSaver(temp_json_file)
        assert saver.get_aeroplanes({}) == []


class TestJSONSaverDelete:
    def test_delete_existing(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        saver.delete_aeroplane(sample_aeroplanes[1])  # AFL123
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 2
        assert all(item["callsign"] != "AFL123" for item in data)

    def test_delete_nonexistent(self, temp_json_file, sample_aeroplanes):
        saver = JSONSaver(temp_json_file)
        saver.add_aeroplanes(sample_aeroplanes)
        missing = Aeroplane("MISSING", "Spain", 100.0, 1000.0)
        saver.delete_aeroplane(missing)  # не должно упасть
        with open(temp_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 3


class TestJSONSaverFileHandling:
    def test_read_nonexistent_file(self, temp_json_file):
        saver = JSONSaver(temp_json_file)
        assert saver._read_file() == []

    def test_read_invalid_json(self, temp_json_file):
        with open(temp_json_file, "w", encoding="utf-8") as f:
            f.write("not a json {")
        saver = JSONSaver(temp_json_file)
        assert saver._read_file() == []
