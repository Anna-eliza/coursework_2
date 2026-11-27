class Aeroplane:
    """Класс для представления информации о самолете."""

    def __init__(self, callsign: str, origin_country: str, velocity: float, altitude: float):
        if callsign is None:
            callsign = "Unknown"
        elif isinstance(callsign, str):
            callsign = callsign.strip()
        else:
            raise ValueError("Позывной должен быть строкой или None")
        if not isinstance(origin_country, str):
            raise ValueError("Страна регистрации должна быть строкой")

        if not isinstance(velocity, (int, float)):
            raise ValueError("Скорость должна быть числом")
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")

        if not isinstance(altitude, (int, float)):
            raise ValueError("Высота должна быть числом")
        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

        self.__callsign = callsign
        self.__origin_country = origin_country
        self.__velocity = velocity
        self.__altitude = altitude

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def altitude(self) -> float:
        return self.__altitude

    @classmethod
    def cast_to_object_list(cls, data: list) -> list:
        """Преобразует сырые данные от opensky в список объектов Aeroplane."""
        aeroplanes = []
        for item in data:
            try:
                callsign = item[1]
                origin_country = item[2]
                velocity = item[9]
                altitude = item[7]

                if velocity is None:
                    velocity = 0.0
                if altitude is None:
                    altitude = 0.0

                aeroplane = cls(callsign, origin_country, velocity, altitude)
                aeroplanes.append(aeroplane)
            except (IndexError, ValueError, TypeError):
                continue

        return aeroplanes

    def __eq__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__velocity == other.velocity

    def __lt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__velocity < other.velocity

    def __gt__(self, other):
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.__velocity > other.velocity

    def is_higher_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с другим самолетом")
        return self.__altitude > other.altitude

    def is_lower_than(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с другим самолетом")
        return self.__altitude < other.altitude
