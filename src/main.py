from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.file_saver import JSONSaver


def user_interaction():
    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны: ")

    raw_data = api.get_aeroplanes(country)
    if not raw_data:
        print("Самолеты не найдены.")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_data)

    if not aeroplanes:
        print("Не удалось обработать данные о самолетах.")
        return

    saver.add_aeroplanes(aeroplanes)
    print(f"\nДанные о {len(aeroplanes)} самолетах сохранены в файл.")

    try:
        top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    except ValueError:
        print("Некорректный ввод. Вывожу топ 5.")
        top_n = 5

    sorted_by_altitude = sorted(aeroplanes, key=lambda a: a.altitude, reverse=True)
    top = sorted_by_altitude[:top_n]

    print(f"\nТоп {top_n} самолетов по высоте:")
    for a in top:
        print(f"{a.callsign} | {a.origin_country} | {a.velocity} м/с | {a.altitude} м")

    countries_input = input("\nВведите страны для фильтрации (через пробел): ")
    countries = [c.lower() for c in countries_input.split()]

    if countries:
        filtered = [a for a in aeroplanes if a.origin_country.lower() in countries]
        if not filtered:
            print("Самолеты по заданным странам не найдены.")
        else:
            print("\nОтфильтрованные самолеты:")
            for a in filtered:
                print(f"{a.callsign} | {a.origin_country} | {a.velocity} м/с | {a.altitude} м")
    else:
        print("Фильтрация не задана.")

if __name__ == "__main__":
    user_interaction()
