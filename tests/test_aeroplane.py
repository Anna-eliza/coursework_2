import pytest
from src.aeroplane import Aeroplane


class TestAeroplaneInit:
    def test_valid_data(self):
        a = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        assert a.callsign == "UAL1621"
        assert a.origin_country == "United States"
        assert a.velocity == 268.79
        assert a.altitude == 10203.18

    def test_callsign_none_becomes_unknown(self):
        a = Aeroplane(None, "Spain", 100.0, 1000.0)
        assert a.callsign == "Unknown"

    def test_callsign_strip(self):
        a = Aeroplane("  ABC123  ", "Spain", 100.0, 1000.0)
        assert a.callsign == "ABC123"

    def test_callsign_not_string_raises(self):
        with pytest.raises(ValueError):
            Aeroplane(123, "Spain", 100.0, 1000.0)

    def test_origin_country_not_string_raises(self):
        with pytest.raises(ValueError):
            Aeroplane("A1", 123, 100.0, 1000.0)

    def test_negative_velocity_raises(self):
        with pytest.raises(ValueError):
            Aeroplane("A1", "Spain", -10.0, 1000.0)

    def test_negative_altitude_raises(self):
        with pytest.raises(ValueError):
            Aeroplane("A1", "Spain", 100.0, -500.0)

    def test_velocity_not_number_raises(self):
        with pytest.raises(ValueError):
            Aeroplane("A1", "Spain", "fast", 1000.0)

    def test_altitude_not_number_raises(self):
        with pytest.raises(ValueError):
            Aeroplane("A1", "Spain", 100.0, "high")


class TestAeroplaneComparison:
    def test_less_than_by_velocity(self):
        a1 = Aeroplane("A1", "Spain", 100.0, 1000.0)
        a2 = Aeroplane("A2", "Spain", 200.0, 1000.0)
        assert a1 < a2
        assert not (a2 < a1)

    def test_greater_than_by_velocity(self):
        a1 = Aeroplane("A1", "Spain", 100.0, 1000.0)
        a2 = Aeroplane("A2", "Spain", 200.0, 1000.0)
        assert a2 > a1

    def test_equal_by_velocity(self):
        a1 = Aeroplane("A1", "Spain", 100.0, 1000.0)
        a2 = Aeroplane("A2", "France", 100.0, 2000.0)
        assert a1 == a2

    def test_comparison_with_non_aeroplane_returns_notimplemented(self):
        a = Aeroplane("A1", "Spain", 100.0, 1000.0)
        assert a.__eq__(123) is NotImplemented
        assert a.__lt__(123) is NotImplemented
        assert a.__gt__(123) is NotImplemented

    def test_is_higher_than(self):
        a1 = Aeroplane("A1", "Spain", 100.0, 5000.0)
        a2 = Aeroplane("A2", "Spain", 100.0, 1000.0)
        assert a1.is_higher_than(a2)
        assert not a2.is_higher_than(a1)

    def test_is_lower_than(self):
        a1 = Aeroplane("A1", "Spain", 100.0, 5000.0)
        a2 = Aeroplane("A2", "Spain", 100.0, 1000.0)
        assert a2.is_lower_than(a1)

    def test_is_higher_than_non_aeroplane_raises(self):
        a = Aeroplane("A1", "Spain", 100.0, 1000.0)
        with pytest.raises(TypeError):
            a.is_higher_than(123)


class TestCastToObjectList:
    def test_cast_valid_data(self, raw_opensky_data):
        result = Aeroplane.cast_to_object_list(raw_opensky_data)
        assert len(result) == 3
        assert result[0].callsign == "TVF22UT"
        assert result[0].origin_country == "France"
        assert result[0].velocity == 209.09
        assert result[0].altitude == 11567.16

    def test_cast_handles_none_callsign(self, raw_opensky_data):
        result = Aeroplane.cast_to_object_list(raw_opensky_data)
        assert result[1].callsign == "Unknown"

    def test_cast_handles_none_velocity_altitude(self):
        raw = [['id', 'CS', 'Spain', 0, 0, 0, 0, None, False, None, 0, 0, None, None, '0000', False, 0]]
        result = Aeroplane.cast_to_object_list(raw)
        assert len(result) == 1
        assert result[0].velocity == 0.0
        assert result[0].altitude == 0.0

    def test_cast_skips_invalid_records(self):
        raw = [
            ['id', 'CS'],
            ['id', 'CS2', 'Spain', 0, 0, 0, 0, 1000, False, 100, 0, 0, None, None, '0000', False, 0],
        ]
        result = Aeroplane.cast_to_object_list(raw)
        assert len(result) == 1
        assert result[0].callsign == "CS2"

    def test_cast_empty_list(self):
        assert Aeroplane.cast_to_object_list([]) == []
