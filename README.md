# 1. Создание локального репозитория
Создайте репозиторий с расширением .git на устройстве:

```bash
cd <директория будущего проекта>
git init
```

# 2. Установка зависимостей и запуск
Для дальнейшего построения графа, добавим коммиты к локальному репозиторию
# Создадим файлы, подтверждая свои действия коммитами

```bash
$ echo "print('Hello, world!')" > prog.py
#Добавляем в репозиторий программу
$ git add prog1.py
#Добавляем коммит
$ git commit -m "Add prog1.py"

$ echo "123456789" > test.txt
#Добавляем в репозиторий текстовый файл
$ git add test.txt
#Добавляем коммит
$ git commit -m "Add file test.txt"

$ echo -e "\n## Authors\n- Muver1" >> readme.md
#Добавляем в репозиторий файл с расширением .md
$ git add readme.md
#Добавляем коммит
$ git commit -m "Add info about authors"
```

#  Запуск
Запуск программы производится через команду в консоли, в нашем случаи в Windows.

```bash
$ py /path/to/visualizer.py --plantuml_tool /path/to/plantuml.jar --repo_path /path/to/repo.git --output_path /path/to/result.uml
```
# 3. Структура проекта
Проект содержит следующие файлы и директории, связанные с тестированием:

```bash
visualizer.py           # Файл с реализацией команд
tests.py      # Файл с тестами для команд
```

# 4. Запуск тестов
В этом руководстве описывается, как запустить тесты для построения графа зависимостей. Мы будем использовать модуль Python ```pytest -v``` для тестирования.
```
pytest -v
```