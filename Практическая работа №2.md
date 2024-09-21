# Minkov-Andrey-IKBO-62-23 Практическая работа №2

## Задача 1

Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

![image](https://github.com/user-attachments/assets/799a2a67-170b-4f42-8a05-ec162fe8af4c)

Один из способов установить пакет без использования менеджера пакетов — это клонировать репозиторий в временную папку, а затем выполнить установку пакета из этой директории, используя команду python setup.py install.

## Задача 2

Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория

![image](https://github.com/user-attachments/assets/776c3d07-3d32-4196-9340-e6456e42ef6e)

## Задача 3

Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.

Создадим файл md.dot и ed.dot с указанием зависимостей между библиотеками
```bash
digraph G {
    rankdir=LR;
    node [shape=ellipse, style=filled, color=lightblue];

    "matplotlib" -> "numpy";
    "matplotlib" -> "pillow";
    "matplotlib" -> "cycler";
    "matplotlib" -> "kiwisolver";
    "matplotlib" -> "pyparsing";
    "matplotlib" -> "python-dateutil";
}
```

```bash
digraph G {
    rankdir=LR;
    node [shape=ellipse, style=filled, color=lightgreen];

    "express" -> "accepts";
    "express" -> "array-flatten";
    "express" -> "body-parser";
    "express" -> "content-disposition";
    "express" -> "cookie";
    "express" -> "cookie-signature";
    "express" -> "debug";
    "express" -> "depd";
    "express" -> "encodeurl";
    "express" -> "escape-html";
    "express" -> "etag";
    "express" -> "finalhandler";
    "express" -> "fresh";
    "express" -> "merge-descriptors";
    "express" -> "methods";
    "express" -> "on-finished";
    "express" -> "parseurl";
    "express" -> "path-to-regexp";
    "express" -> "proxy-addr";
    "express" -> "qs";
    "express" -> "range-parser";
    "express" -> "safe-buffer";
    "express" -> "send";
    "express" -> "serve-static";
    "express" -> "setprototypeof";
    "express" -> "statuses";
    "express" -> "type-is";
    "express" -> "utils-merge";
    "express" -> "vary";
}
```
 Генерация графика для matplotlib
 ```bash
$ dot -Tpng md.dot -o matplotlib_dependencies.png
```
![matplotlib_dependencies](https://github.com/user-attachments/assets/15cea608-bae9-48fb-8000-d300fe03473d)

 Генерация графика для express
 ```bash
$ dot -Tpng ed.dot -o express_dependencies.png
```
![express_dependencies](https://github.com/user-attachments/assets/cfebff75-21c5-4c6b-9541-b9d105fe2ef6)
# Задание №4

Следующие задачи можно решать с помощью инструментов на выбор:

Решатель задачи удовлетворения ограничениям (MiniZinc).
SAT-решатель (MiniSAT).
SMT-решатель (Z3).
Изучить основы программирования в ограничениях. Установить MiniZinc, разобраться с основами его синтаксиса и работы в IDE.

Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте all_different). Найти минимальное решение для суммы 3 цифр.

```bash
include "alldifferent.mzn";

var 1..9: d1;  
var 0..9: d2; 
var 0..9: d3; 
var 0..9: d4; 
var 0..9: d5;  
var 0..9: d6; 

constraint alldifferent([d1, d2, d3, d4, d5, d6]);

constraint d1 + d2 + d3 = d4 + d5 + d6;

solve minimize d1 + d2 + d3; 
```

![image](https://github.com/user-attachments/assets/e982fa5e-bb25-4351-9bf8-a234e3ed01c1)

# Задание №5

Решить на MiniZinc задачу о зависимостях пакетов для рисунка, приведенного ниже.

![image](https://github.com/user-attachments/assets/88df785a-dd78-4fe6-b72d-92aaf9fc39f7)

```bash
% Use this editor as a MiniZinc scratch book
set of int: MenuVersions = 1..6;
set of int: DropdownVersions = 1..5;
set of int: IconVersions = 1..2;

array[MenuVersions] of int: menu = [150, 140, 130, 120, 110, 100];
array[DropdownVersions] of int: dropdown = [230, 220, 210, 200, 180];
array[IconVersions] of int: icons = [200, 100];

var MenuVersions: selected_menu;
var DropdownVersions: selected_dropdown;
var IconVersions: selected_icons;

constraint
    (selected_menu = 1 -> selected_dropdown in 1..3) /\
    (selected_menu = 2 -> selected_dropdown in 2..4) /\
    (selected_menu = 3 -> selected_dropdown in 3..5) /\
    (selected_menu = 4 -> selected_dropdown in 4..5) /\
    (selected_menu = 5 -> selected_dropdown = 5) /\
    (selected_dropdown = 1 -> selected_icons = 1) /\
    (selected_dropdown = 2 -> selected_icons in 1..2) /\
    (selected_dropdown = 3 -> selected_icons in 1..2) /\
    (selected_dropdown = 4 -> selected_icons in 1..2) /\
    (selected_dropdown = 5 -> selected_icons in 1..2);

solve satisfy;

output [
    "Selected menu version: \(menu[selected_menu])\n",
    "Selected dropdown version: \(dropdown[selected_dropdown])\n",
    "Selected icon version: \(icons[selected_icons])\n"
];
```

![image](https://github.com/user-attachments/assets/348a6f13-ff67-44fc-85e2-5f99a386ade2)

# Задание №6

Решить на MiniZinc задачу о зависимостях пакетов для следующих данных:

```
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0.
foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0.
foo 1.0.0 не имеет зависимостей.
left 1.0.0 зависит от shared >=1.0.0.
right 1.0.0 зависит от shared <2.0.0.
shared 2.0.0 не имеет зависимостей.
shared 1.0.0 зависит от target ^1.0.0.
target 2.0.0 и 1.0.0 не имеют зависимостей.
```
```bash
include "alldifferent.mzn";

% Пакеты и их версии
var 1..1: root_version;  % версия пакета root
var 1..2: foo_version;  % версия пакета foo
var 1..2: left_version;  % версия пакета left
var 1..2: right_version;  % версия пакета right
var 1..2: shared_version;  % версия пакета shared
var 1..2: target_version;  % версия пакета target

% Зависимости между пакетами
constraint (root_version == 1) -> (foo_version == 1 \/ foo_version == 2);
constraint (root_version == 1) -> (target_version == 2);
constraint (foo_version == 2) -> (left_version == 1);
constraint (foo_version == 2) -> (right_version == 1);
constraint (left_version == 1) -> (shared_version == 1 \/ shared_version == 2);
constraint (right_version == 1) -> (shared_version == 1);
constraint (shared_version == 1) -> (target_version == 1 \/ target_version == 2);

% Решение
solve satisfy;
```

![image](https://github.com/user-attachments/assets/048fedb0-2605-4e9f-8993-ead96bedd705)

# Задание №7

Представить задачу о зависимостях пакетов в общей форме. Здесь необходимо действовать аналогично реальному менеджеру пакетов. То есть получить описание пакета, а также его зависимости в виде структуры данных. Например, в виде словаря. В предыдущих задачах зависимости были явно заданы в системе ограничений. Теперь же систему ограничений надо построить автоматически, по метаданным.

```bash
int: num_packages;

set of int: Packages = 1..num_packages;

array[Packages] of set of int: Versions;

array[Packages] of var int: selected_version;

array[Packages] of set of int: dependencies;

array[Packages, Packages] of int: min_version;

array[Packages, Packages] of int: max_version;

constraint
  forall(i in Packages) (
    forall(dep in dependencies[i]) (
      selected_version[dep] >= min_version[i, dep] /\
      selected_version[dep] <= max_version[i, dep]
    )
  );

solve satisfy;
```

![image](https://github.com/user-attachments/assets/126c0517-9a1b-4c10-8bf7-883dbdbcb911)
