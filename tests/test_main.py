import pytest
from unittest.mock import patch
from src.main import user_interaction


@patch("src.main.JSONSaver")
@patch("src.main.AeroplanesAPI")
@patch("builtins.input")
def test_user_interaction_happy_path(mock_input, mock_api_class, mock_saver_class, capsys):
    """Тест успешного сценария: данные получены, топ выведен, фильтр сработал."""
    mock_input.side_effect = ["Spain", "2", "Spain France"]

    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_aeroplanes.return_value = [
        ['id1', 'CS1', 'Spain', 0, 0, 0, 0, 10000, False, 200, 0, 0, None, None, '0000', False, 0],
        ['id2', 'CS2', 'France', 0, 0, 0, 0, 15000, False, 250, 0, 0, None, None, '0000', False, 0],
    ]

    user_interaction()

    mock_saver_instance = mock_saver_class.return_value
    mock_saver_instance.add_aeroplanes.assert_called_once()
    saved = mock_saver_instance.add_aeroplanes.call_args[0][0]
    assert len(saved) == 2

    captured = capsys.readouterr()
    assert "Топ 2 самолетов по высоте:" in captured.out
    assert "CS2" in captured.out
    assert "CS1" in captured.out
    assert "Отфильтрованные самолеты:" in captured.out


@patch("src.main.JSONSaver")
@patch("src.main.AeroplanesAPI")
@patch("builtins.input", return_value="NotACountry")
def test_user_interaction_no_aeroplanes(mock_input, mock_api_class, mock_saver_class, capsys):
    """Тест: API вернул пустой список — программа должна сообщить об этом."""
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_aeroplanes.return_value = []

    user_interaction()

    captured = capsys.readouterr()
    assert "Самолеты не найдены." in captured.out


@patch("src.main.JSONSaver")
@patch("src.main.AeroplanesAPI")
@patch("builtins.input")
def test_user_interaction_invalid_top_n(mock_input, mock_api_class, mock_saver_class, capsys):
    """Тест: пользователь ввёл не число для N — программа не падает, использует 5."""
    mock_input.side_effect = ["Spain", "abc", ""]  # "abc" — некорректный ввод
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_aeroplanes.return_value = [
        ['id', 'CS', 'Spain', 0, 0, 0, 0, 1000, False, 100, 0, 0, None, None, '0000', False, 0]
    ]

    user_interaction()

    captured = capsys.readouterr()
    assert "Некорректный ввод" in captured.out
    assert "Топ 5 самолетов по высоте:" in captured.out


@patch("src.main.JSONSaver")
@patch("src.main.AeroplanesAPI")
@patch("builtins.input")
def test_user_interaction_no_filter(mock_input, mock_api_class, mock_saver_class, capsys):
    """Тест: пользователь не ввёл страны для фильтрации."""
    mock_input.side_effect = ["Spain", "1", ""]
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_aeroplanes.return_value = [
        ['id', 'CS', 'Spain', 0, 0, 0, 0, 1000, False, 100, 0, 0, None, None, '0000', False, 0]
    ]

    user_interaction()

    captured = capsys.readouterr()
    assert "Фильтрация не задана." in captured.out


@patch("src.main.JSONSaver")
@patch("src.main.AeroplanesAPI")
@patch("builtins.input")
def test_user_interaction_filter_not_found(mock_input, mock_api_class, mock_saver_class, capsys):
    """Тест: фильтрация не нашла ни одного самолета."""
    mock_input.side_effect = ["Spain", "1", "Germany"]
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.get_aeroplanes.return_value = [
        ['id', 'CS', 'Spain', 0, 0, 0, 0, 1000, False, 100, 0, 0, None, None, '0000', False, 0]
    ]

    user_interaction()

    captured = capsys.readouterr()
    assert "Самолеты по заданным странам не найдены." in captured.out
