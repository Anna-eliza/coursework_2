from abc import ABC, abstractmethod
from src.aeroplane import Aeroplane
import json
import os


class BaseSaver(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет информацию о самолете в файл."""
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: dict) -> list:
        """Получает данные из файла по указанным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет информацию о самолете из файла."""
        pass


class JSONSaver(BaseSaver):
    def __init__(self, filename: str = "aeroplanes.json"):
        self.__filename = filename

    def _read_file(self) -> list:
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write_file(self, data: list) -> None:
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        aeroplane_dict = {
            "callsign": aeroplane.callsign,
            "origin_country": aeroplane.origin_country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude
        }
        data = self._read_file()
        data.append(aeroplane_dict)
        self._write_file(data)

    def add_aeroplanes(self, aeroplanes: list) -> None:
        data = self._read_file()
        for a in aeroplanes:
            data.append({
                "callsign": a.callsign,
                "origin_country": a.origin_country,
                "velocity": a.velocity,
                "altitude": a.altitude
            })
        self._write_file(data)

    def get_aeroplanes(self, criteria: dict) -> list:
        data = self._read_file()
        result = []

        for item in data:
            if "origin_country" in criteria and item["origin_country"] != criteria["origin_country"]:
                continue
            if "velocity_min" in criteria and item["velocity"] < criteria["velocity_min"]:
                continue
            if "velocity_max" in criteria and item["velocity"] > criteria["velocity_max"]:
                continue
            if "altitude_min" in criteria and item["altitude"] < criteria["altitude_min"]:
                continue
            if "altitude_max" in criteria and item["altitude"] > criteria["altitude_max"]:
                continue

            result.append(item)

        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_file()

        new_data = [item for item in data if item["callsign"] != aeroplane.callsign]

        self._write_file(new_data)
