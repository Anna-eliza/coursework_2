import pytest
import os
from src.aeroplane import Aeroplane


@pytest.fixture
def sample_aeroplanes():
    """Список объектов Aeroplane для тестов."""
    return [
        Aeroplane("UAL1621", "United States", 268.79, 10203.18),
        Aeroplane("AFL123", "Russia", 300.0, 11000.0),
        Aeroplane("TVF22UT", "France", 209.09, 11567.16),
    ]


@pytest.fixture
def raw_opensky_data():
    """Сырые данные от opensky (в формате списка списков)."""
    return [
        ['39de4a', 'TVF22UT ', 'France', 1795600514, 1795600514, -4.7552, 39.1718, 11567.16, False, 209.09, 17.32, 0, None, 11704.32, '6456', False, 0],
        ['a1b2c3', None, 'Spain', 1795600515, 1795600515, 2.3522, 48.8566, 1000.0, False, 250.0, 0.0, 0, None, 1020.0, '1234', False, 0],
        ['d4e5f6', 'AFL123', 'Russia', 1795600516, 1795600516, 30.0, 60.0, 11000.0, False, 300.0, 10.0, 0, None, 11200.0, '5678', False, 0],
    ]


@pytest.fixture
def temp_json_file(tmp_path):
    """Путь к временному JSON-файлу, который удаляется после теста."""
    return str(tmp_path / "test_aeroplanes.json")


@pytest.fixture
def empty_json_file(temp_json_file):
    """Создаёт пустой JSON-файл (список) и возвращает путь."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("[]")
    return temp_json_file
