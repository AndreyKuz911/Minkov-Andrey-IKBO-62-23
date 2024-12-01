import sys
import toml
import re


class ConfigLanguageConverter:
    def __init__(self):
        self.constants = {}

    def parse_constant(self, key, value):
        """Сохраняет константы в таблицу."""
        if re.fullmatch(r"[_a-zA-Z]+", key):
            self.constants[key] = self.convert_value(value)
        else:
            raise ValueError(f"Некорректное имя константы: {key}")

    def resolve_constant(self, expression):
        """Возвращает значение для выражений с `@[имя]`."""
        match = re.match(r"@\[([_a-zA-Z]+)\]", expression)
        if match:
            const_name = match.group(1)
            if const_name in self.constants:
                return f"{self.constants[const_name]} => @{const_name}"
            else:
                raise ValueError(f"Неопределенная константа: {const_name}")
        return expression

    def convert_value(self, value):
        """Рекурсивно преобразует значения в целевой формат."""
        if isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Проверка на использование константы
            if value.startswith("@["):
                return self.resolve_constant(value)
            return value
        elif isinstance(value, list):
            return f"<< {', '.join(self.convert_value(v) for v in value)} >>"
        elif isinstance(value, dict):
            items = [f"  {k} : {self.convert_value(v)};" for k, v in value.items()]
            return "{\n" + "\n".join(items) + "\n}"
        else:
            raise ValueError(f"Некорректное значение: {value}")

    def convert(self, toml_data, comments=None):
        """Конвертирует TOML в учебный конфигурационный язык."""
        output = []
        const_output = []

        # Вставка комментария
        if comments:
            output.append("=begin")
            output.extend(comments)
            output.append("=end\n")

        # Первый проход: сохранение констант
        for key, value in toml_data.items():
            if not isinstance(value, (dict, list)) and not (isinstance(value, str) and value.startswith("@[")):
                self.parse_constant(key, value)

        # Второй проход: обработка оставшихся данных
        for key, value in toml_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                output.append(f"{key} = {self.convert_value(value)}")
            elif isinstance(value, (int, float, str)) and not (isinstance(value, str) and value.startswith("@[")):
                output.append(f"{key} = {self.convert_value(value)}")
            elif isinstance(value, str) and value.startswith("@["):
                const_output.append(self.resolve_constant(value))

        # Добавляем отдельно упоминания констант в формате `значение => @[имя]`
        for const_name, const_value in self.constants.items():
            const_output.append(f"{const_value} => @{const_name}")

        output.extend(const_output)
        return "\n".join(output)


def main():
    try:
        # Чтение TOML из стандартного ввода
        input_toml = sys.stdin.read()

        # Пример многострочного комментария
        comments = [
            "Это многострочный",
            "комментарий",
        ]

        # Загрузка данных TOML
        toml_data = toml.loads(input_toml)

        # Создание объекта конвертера
        converter = ConfigLanguageConverter()

        # Преобразование данных
        result = converter.convert(toml_data, comments=comments)

        # Вывод результата
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
