import pytest
from unittest.mock import patch, MagicMock
from src.api import AeroplanesAPI


class TestGetCountryCoordinates:
    @patch("src.api.requests.get")
    def test_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"boundingbox": ["35.0", "43.0", "-9.0", "3.0"]}
        ]
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        result = api.get_country_coordinates("Spain")
        assert result == [35.0, 43.0, -9.0, 3.0]

    @patch("src.api.requests.get")
    def test_network_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network down")

        api = AeroplanesAPI()
        result = api.get_country_coordinates("Spain")
        assert result == []

    @patch("src.api.requests.get")
    def test_empty_result(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        result = api.get_country_coordinates("NotACountry")
        assert result == []


class TestGetAeroplanes:
    @patch("src.api.requests.get")
    def test_success(self, mock_get):
        nominatim_response = MagicMock()
        nominatim_response.status_code = 200
        nominatim_response.json.return_value = [
            {"boundingbox": ["35.0", "43.0", "-9.0", "3.0"]}
        ]

        opensky_response = MagicMock()
        opensky_response.status_code = 200
        opensky_response.json.return_value = {
            "states": [["id", "CS", "Spain", 0, 0, 0, 0, 1000, False, 100, 0, 0, None, None, "0000", False, 0]]
        }

        mock_get.side_effect = [nominatim_response, opensky_response]

        api = AeroplanesAPI()
        result = api.get_aeroplanes("Spain")
        assert len(result) == 1
        assert result[0][1] == "CS"

    @patch("src.api.requests.get")
    def test_no_coordinates(self, mock_get):
        nominatim_response = MagicMock()
        nominatim_response.status_code = 200
        nominatim_response.json.return_value = []
        mock_get.return_value = nominatim_response

        api = AeroplanesAPI()
        result = api.get_aeroplanes("NotACountry")
        assert result == []

    @patch("src.api.requests.get")
    def test_opensky_empty_states(self, mock_get):
        nominatim_response = MagicMock()
        nominatim_response.status_code = 200
        nominatim_response.json.return_value = [
            {"boundingbox": ["35.0", "43.0", "-9.0", "3.0"]}
        ]

        opensky_response = MagicMock()
        opensky_response.status_code = 200
        opensky_response.json.return_value = {"states": None}

        mock_get.side_effect = [nominatim_response, opensky_response]

        api = AeroplanesAPI()
        result = api.get_aeroplanes("Spain")
        assert result == []
