"""
Калькулятор с преобразованием в обратную польскую нотацию
Поддерживает унарный минус и возведение в степень
"""

import operator
from typing import List, Union

class Calculator:
    """Калькулятор с поддержкой ОПН и унарных операторов"""

    def __init__(self):
        # Приоритет операторов (чем выше число, тем выше приоритет)
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '^': 3,
            'u': 4  # Унарный минус
        }

        # Операторы и соответствующие функции
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '^': operator.pow,
            'u': lambda x: -x
        }

    def calculate(self, expression: str) -> float:
        """
        Вычисляет математическое выражение с выводом в консоль

        Args:
            expression: Строка с математическим выражением

        Returns:
            Результат вычисления

        Raises:
            ValueError: При неверном выражении
            ZeroDivisionError: При делении на ноль
        """
        if not expression or expression.strip() == "":
            raise ValueError("Expression cannot be empty")

        print(f"\n🧮 Вычисление выражения: {expression}")
        print("=" * 50)

        # Преобразуем в ОПН
        rpn = self.to_reverse_polish_notation(expression)
        print(f"📋 Обратная польская запись: {' '.join(rpn)}")

        # Вычисляем результат
        result = self.evaluate_rpn(rpn)
        print(f"✅ Результат: {result}")
        print("=" * 50)

        return result

    def to_reverse_polish_notation(self, expression: str) -> List[str]:
        """
        Преобразует инфиксную нотацию в обратную польскую нотацию

        Args:
            expression: Выражение в инфиксной нотации

        Returns:
            Список токенов в ОПН
        """
        output = []
        stack = []
        tokens = self._tokenize(expression)
        may_be_unary = True  # Флаг для определения унарного минуса

        for token in tokens:
            if self._is_number(token):
                output.append(token)
                may_be_unary = False
            elif self._is_operator(token):
                # Проверяем, является ли минус унарным
                if may_be_unary and token == '-':
                    token = 'u'

                # Выталкиваем операторы с более высоким или равным приоритетом
                # Для право-ассоциативных операторов (^) используем строгое неравенство
                while (stack and self._is_operator(stack[-1]) and
                       ((self._get_precedence(token) < self._get_precedence(stack[-1])) or
                        (self._get_precedence(token) == self._get_precedence(stack[-1]) and
                         self._is_left_associative(token)))):
                    output.append(stack.pop())

                stack.append(token)
                may_be_unary = True
            elif token == '(':
                stack.append(token)
                may_be_unary = True
            elif token == ')':
                # Выталкиваем все операторы до открывающей скобки
                while stack and stack[-1] != '(':
                    output.append(stack.pop())

                if not stack:
                    raise ValueError("Mismatched parentheses")

                stack.pop()  # Удаляем '('
                may_be_unary = False

        # Выталкиваем оставшиеся операторы
        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(stack.pop())

        return output

    def evaluate_rpn(self, rpn: List[str]) -> float:
        """
        Вычисляет выражение в обратной польской нотации

        Args:
            rpn: Список токенов в ОПН

        Returns:
            Результат вычисления
        """
        stack = []

        for token in rpn:
            if self._is_number(token):
                stack.append(float(token))
            elif self._is_operator(token):
                if token == 'u':
                    # Унарный оператор - один операнд
                    if not stack:
                        raise ValueError("Insufficient operands for unary operator")
                    operand = stack.pop()
                    result = self.operators[token](operand)
                    stack.append(result)
                else:
                    # Бинарный оператор - два операнда
                    if len(stack) < 2:
                        raise ValueError("Insufficient operands for binary operator")
                    right = stack.pop()
                    left = stack.pop()

                    if token == '/' and right == 0:
                        raise ZeroDivisionError("Division by zero")

                    result = self.operators[token](left, right)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack[0]

    def _tokenize(self, expression: str) -> List[str]:
        """Разбивает выражение на токены"""
        tokens = []
        current = []
        expression = expression.replace(' ', '')

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or char == '.':
                current.append(char)
            else:
                if current:
                    tokens.append(''.join(current))
                    current = []

                # Обработка унарного минуса
                if (char == '-' and
                    (i == 0 or
                     expression[i-1] == '(' or
                     self._is_operator(expression[i-1]))):
                    tokens.append('-')  # Будет обработан как унарный в RPN
                else:
                    tokens.append(char)

            i += 1

        if current:
            tokens.append(''.join(current))

        return tokens

    def _is_number(self, token: str) -> bool:
        """Проверяет, является ли токен числом"""
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _is_operator(self, token: str) -> bool:
        """Проверяет, является ли токен оператором"""
        return token in self.precedence or token in ['-', '+', '*', '/', '%', '^']

    def _get_precedence(self, operator: str) -> int:
        """Возвращает приоритет оператора"""
        return self.precedence.get(operator, 0)

    def _is_left_associative(self, operator: str) -> bool:
        """Проверяет, является ли оператор лево-ассоциативным"""
        # Возведение в степень - право-ассоциативно
        # Остальные операторы - лево-ассоциативные
        return operator != '^'


def main():
    """
    Основная функция для ручного ввода выражений
    """
    calc = Calculator()

    print("🧮 КАЛЬКУЛЯТОР С ОБРАТНОЙ ПОЛЬСКОЙ ЗАПИСЬЮ")
    print("=" * 60)
    print("Поддерживаемые операции: +, -, *, /, %, ^ (степень), унарный минус")
    print("Примеры: 2 + 3 * 4, (1 + 2) * 3, -5 + 8, 2 ^ 3")
    print("Для выхода введите 'quit', 'exit' или нажмите Ctrl+C")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nВведите выражение: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 До свидания!")
                break

            if not user_input:
                print("⚠️  Пустой ввод. Попробуйте снова.")
                continue

            result = calc.calculate(user_input)

        except KeyboardInterrupt:
            print("\n\n👋 До свидания!")
            break
        except ZeroDivisionError as e:
            print(f"❌ Ошибка: {e}")
        except ValueError as e:
            print(f"❌ Ошибка в выражении: {e}")
        except Exception as e:
            print(f"❌ Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()