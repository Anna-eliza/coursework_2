from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> list:
        """Получение координат страны (boundingbox)."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> list:
        """Получение информации о самолетах в воздушном пространстве страны."""
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для работы с API nominatim и opensky."""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def get_country_coordinates(self, country_name: str) -> list:
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "coursework-2/1.0"
        }
        try:
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            boundingbox = data[0]["boundingbox"]
            return [float(x) for x in boundingbox]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к nominatim: {e}")
            return []
        except (ValueError, IndexError, KeyError) as e:
            print(f"Ошибка обработки ответа: {e}")
            return []

    def get_aeroplanes(self, country_name: str) -> list:
        coords = self.get_country_coordinates(country_name)
        if not coords:
            return []
        params = {
            "lamin": coords[0],
            "lamax": coords[1],
            "lomin": coords[2],
            "lomax": coords[3]
        }
        try:
            response = requests.get(self.opensky_url, params=params)
            response.raise_for_status()
            data = response.json()
            states = data.get("states", [])
            if states is None:
                return []
            return states
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к opensky: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Ошибка обработки ответа: {e}")
            return []
