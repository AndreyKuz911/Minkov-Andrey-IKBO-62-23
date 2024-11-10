import toml
import re
import sys

class ConfigTranslator:
    def __init__(self, toml_data):
        self.data = toml_data
        self.constants = {}

    def translate(self):
        result = self.translate_section(self.data)
        return result

    def translate_section(self, section):
        translated = []
        for key, value in section.items():
            if isinstance(value, dict):
                # Обработка словаря
                translated.append(f"{key} = {self.translate_dict(value)}")
            elif isinstance(value, list):
                # Обработка массива
                translated.append(f"{key} = {self.translate_array(value)}")
            elif isinstance(value, (int, float)):
                # Числовое значение
                translated.append(f"{key} = {value}")
            elif isinstance(value, str) and key.startswith('@'):
                # Обработка вычисляемых значений констант
                translated.append(f"@[{key[1:]}] = {self.constants.get(key[1:], 'undefined')}")
            else:
                raise ValueError(f"Unsupported data type for key {key}")
        return "\n".join(translated)

    def translate_dict(self, dictionary):
        result = "{\n"
        for k, v in dictionary.items():
            result += f"    {k} : {self.format_value(v)};\n"
        result += "}"
        return result

    def translate_array(self, array):
        result = "<< "
        result += ", ".join(self.format_value(v) for v in array)
        result += " >>"
        return result

    def format_value(self, value):
        if isinstance(value, dict):
            return self.translate_dict(value)
        elif isinstance(value, list):
            return self.translate_array(value)
        elif isinstance(value, bool):  # Обрабатываем булевы значения
            return '"True"' if value else '"False"'  # Возвращаем как строки с кавычками
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            raise ValueError("Unsupported value type in format_value")


def main():
    input_data = sys.stdin.read()
    try:
        toml_data = toml.loads(input_data)
        translator = ConfigTranslator(toml_data)
        output = translator.translate()
        print(output)
    except toml.TomlDecodeError as e:
        print(f"Error in TOML format: {e}")
    except ValueError as e:
        print(f"Translation error: {e}")

if __name__ == "__main__":
    main()