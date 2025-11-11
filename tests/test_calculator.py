import pytest
from unittest.mock import patch
from io import StringIO
from src.calculator import Calculator


class TestCalculator:
    """Тесты для калькулятора"""

    def setup_method(self):
        self.calc = Calculator()

    def test_basic_operations(self):
        """Тест базовых операций"""
        with patch('sys.stdout', new_callable=StringIO):
            assert self.calc.calculate("2 + 3") == 5
            assert self.calc.calculate("3 - 2") == 1
            assert self.calc.calculate("2 * 3") == 6
            assert self.calc.calculate("6 / 3") == 2

    def test_operator_precedence(self):
        """Тест приоритета операторов"""
        with patch('sys.stdout', new_callable=StringIO):
            assert self.calc.calculate("2 + 3 * 4") == 14
            assert self.calc.calculate("(2 + 3) * 4") == 20
            assert self.calc.calculate("2 * 3 + 4") == 10

    def test_exponentiation(self):
        """Тест возведения в степень"""
        with patch('sys.stdout', new_callable=StringIO):
            assert self.calc.calculate("2 ^ 3") == 8
            assert self.calc.calculate("2 ^ 3 * 4") == 32
            assert self.calc.calculate("2 ^ 3 ^ 2") == 512

    def test_unary_minus(self):
        """Тест унарного минуса"""
        with patch('sys.stdout', new_callable=StringIO):
            assert self.calc.calculate("-5") == -5
            assert self.calc.calculate("2 + -4") == -2
            assert self.calc.calculate("2 * -3") == -6
            assert self.calc.calculate("-2 ^ 3") == -8

    def test_complex_expressions(self):
        """Тест сложных выражений"""
        with patch('sys.stdout', new_callable=StringIO):
            assert self.calc.calculate("(3 + 4) * (5 - 2) + 2") == 23
            assert self.calc.calculate("3.5 * 3") == 10.5
            assert self.calc.calculate("3 + 4 * -2.5") == -7

    def test_rpn_conversion(self):
        """Тест преобразования в ОПН"""
        assert self.calc.to_reverse_polish_notation("3 + 4 * 2") == ['3', '4', '2', '*', '+']
        assert self.calc.to_reverse_polish_notation("(3 + 4) * 2") == ['3', '4', '+', '2', '*']
        assert self.calc.to_reverse_polish_notation("-5 + 3") == ['5', 'u', '3', '+']

    def test_console_output(self):
        """Тест вывода в консоль"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.calc.calculate("2 + 3")
            output = mock_stdout.getvalue()

            assert " Вычисление выражения: 2 + 3" in output
            assert " Обратная польская запись: 2 3 +" in output
            assert " Результат: 5.0" in output
            assert result == 5

    def test_division_by_zero(self):
        """Тест деления на ноль"""
        with patch('sys.stdout', new_callable=StringIO):
            with pytest.raises(ZeroDivisionError):
                self.calc.calculate("5 / 0")

    def test_invalid_expressions(self):
        """Тест неверных выражений"""
        with patch('sys.stdout', new_callable=StringIO):
            with pytest.raises(ValueError):
                self.calc.calculate("")

            with pytest.raises(ValueError):
                self.calc.calculate("2 + + 3")

            with pytest.raises(ValueError):
                self.calc.calculate("(2 + 3")

    def test_mismatched_parentheses(self):
        """Тест несогласованных скобок"""
        with patch('sys.stdout', new_callable=StringIO):
            with pytest.raises(ValueError):
                self.calc.calculate("(2 + 3")

            with pytest.raises(ValueError):
                self.calc.calculate("2 + 3)")


def test_main_function():
    """Тест основной функции"""
    from src.calculator import main
    with patch('builtins.input', side_effect=['2 + 2', 'quit']):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            try:
                main()
            except SystemExit:
                pass
            output = mock_stdout.getvalue()
            assert "КАЛЬКУЛЯТОР С ОБРАТНОЙ ПОЛЬСКОЙ ЗАПИСЬЮ" in output


# Демонстрация провального тестирования
def test_intentional_failure():
    """Этот тест изначально провалится - демонстрация TDD"""
    calc = Calculator()

    # Сначала тест упадёт (раскомментировать для демонстрации)
    # with patch('sys.stdout', new_callable=StringIO):
    #     assert calc.calculate("2 + 2") == 5  # Должно быть 4!

    # Потом исправляем
    with patch('sys.stdout', new_callable=StringIO):
        assert calc.calculate("2 + 2") == 4  # Теперь правильно