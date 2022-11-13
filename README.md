# Лабораторная работа 1 по дисциплине "Технологии программирования"
|Выполнил|Курников Д.С.|
|----------------|----------------|
|Группа|ЭВМ-1.1|
|Вариант|4|
## Цели работы
1. Познакомиться c распределенной системой контроля версий кода Git и ее функциями;
2. Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD), определить их место в современной разработке программного обеспечения;
3. Получить навыки разработки ООП-программ и написания модульных тестов к ним на
современных языках программирования;
4. Получить навыки работы с системой Git для хранения и управления версиями ПО;
5. Получить навыки управления автоматизированным тестированием программного обеспечения,
расположенного в системе Git, с помощью инструмента GitHub Actions.
## Ход работы.
**Индивидуальное задание:** Рассчитать и вывести на экран количество студентов, имеющих академические задолженности (имеющих балл < 61 хотя бы по одному предмету).

**Тип файла c данными:** json.
### Этап 1. Написания кода для чтения json файлов и его тестирование.
Для выполнения первого этапа работы была создана ветка step_1, в которую пушились промежуточные результаты разработки.
#### Создадим файл JsonDataReader.py и реализуем в нём класс JsonDataReader (насследник класса DataReader). Добавим в класс функцию read(), предназначенную для чтения json файлов. Новая функция принимает в качестве аргумента путь к json файлу, если в указанном пути нет файлов требуемого типа, то в консоль будет выведена соответствующая ошибка. Получившийся код представлен ниже.

```python
from Types import DataType
from DataReader import DataReader

class JsonDataReader(DataReader):

    def __init__(self):
        self.key: str = ""
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.endswith(": {"):
                        self.key = line.strip("\" : {")
                        self.students[self.key] = []
                    elif not line.startswith(('{', '}')):
                        subj, score = line.split(":", maxsplit=1)
                        subj = subj.strip("\"")
                        score = score.strip(",")
                        self.students[self.key].append(
                            (subj.strip(), int(score.strip())))
            return self.students

        except FileNotFoundError:
            return {"Error": [("no such file of directory", 1)]}
```
#### Далее, в новом файле test_JsonDataReader.py был создан класс testJsonDataReader, содержащий в себе тесты для приведённого выше блока кода.
```python
class TestJsonDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:

        text = "{\n" + \
         "     \"Иванов Иван Иванович\": {\n" + \
         "         \"математика\": 67,\n" + \
         "         \"литература\": 100,\n" + \
         "         \"программирование\": 91\n" + \
         "     },\n" + \
         "     \"Петров Петр Петрович\": {\n" + \
         "         \"математика\": 78,\n" + \
         "         \"химия\": 87,\n" + \
         "         \"социология\": 61\n" + \
         "     },\n" + "}\n"
        data = {
             "Иванов Иван Иванович": [
                 ("математика", 67), ("литература", 100),
                 ("программирование", 91)
             ],
             "Петров Петр Петрович": [
                 ("математика", 78), ("химия", 87), ("социология", 61)
             ]
         }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: tuple[str, DataType],
                          tmpdir) -> tuple[str, DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.txt")
        p.write_text(file_and_data_content[0], encoding='utf-8')
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = JsonDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]


@pytest.fixture()
def noncoorrect_path_to_file() -> tuple[str, DataType]:
    return "../dat/data.json", {"Error": [("no such file of directory", 1)]}


def test_noncorrect_path_to_file(
        noncoorrect_path_to_file: tuple[str, DataType]) -> None:
    path = JsonDataReader().read(noncoorrect_path_to_file[0])
    assert path == noncoorrect_path_to_file[1]
```
#### Для того чтобы проверить получившийся код, в файл main.py были внесены следующие изменения:
```python
import argparse
import sys

from JsonDataReader import JsonDataReader
from CalcAcademicFailure import CalcAcadFail


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
#    reader = TextDataReader()
    reader = JsonDataReader()
    students = reader.read(path)
    print("Students: ", students)

if __name__ == "__main__":
    main()
```
#### Содержимое файла data.json:
```json
{
     "Иванов Иван Иванович": {
         "математика": 80,
         "литература": 100,
         "программирование": 91
     },
     "Петров Петр Петрович": {
         "математика": 60,
         "химия": 87,
         "социология": 75
     }
}

```
#### Результат работы программы:
```
C:\anaconda3\envs\PTLab1-2022\python.exe C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\src\main.py -p ../data/data.json 
Students:  {'Иванов Иван Иванович': [('математика', 80), ('литература', 100), ('программирование', 91)], 'Петров Петр Петрович': [('математика', 60), ('химия', 87), ('социология', 75)]}

Process finished with exit code 0
```
#### Резуьтаты тестирования:
```
C:\anaconda3\envs\PTLab1-2022\python.exe "C:/Users/Дмитрий/PyCharm Community Edition 2022.2.2/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py" --path C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test\test_JsonDataReader.py 
Testing started at 18:14 ...
Launching pytest with arguments C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test\test_JsonDataReader.py --no-header --no-summary -q in C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test

============================= test session starts =============================
collecting ... collected 2 items

test_JsonDataReader.py::TestJsonDataReader::test_read PASSED             [ 50%]
test_JsonDataReader.py::test_noncorrect_path_to_file PASSED              [100%]

============================== 2 passed in 0.05s ==============================

Process finished with exit code 0
```
#### Коммиты в ветку step_1.
![Коммиты в ветку step_1](https://user-images.githubusercontent.com/61357719/201530542-0cbfde2f-747f-4c34-80ed-ecfa9ce4bade.png)
### Этап 2. Реализация классов, работающих с полученными из json файла данными.
Для реализации блока кода, рассчитывающего академическую задолженность студентов была создана ветка calc_af, в которую пушились промежуточные этапы разработки.
#### Для расчёта академической задолженности студентов в новом файле CalcAcademicFailure.py (содержимое фала представлено ниже), внутри класса CalcAcadFail была создана функция calc(), принимающая на вход данные в формате: list[int, str, dict[str, int]]. Функция calc() возвращает общее число задолжников и число задолженностей у отдельного студента.
```python
from Types import DataType

RatingType = list[int, str, dict[str, int]]


class CalcAcadFail:

    def __init__(self, data: DataType) -> None:
        self.data: DataType = data
        self.rating: RatingType = [0, "Все студенты сдали сессию !", {}]

    def calc(self) -> RatingType:

        for key in self.data:
            self.rating[2][key] = 0
            for rat in self.data[key]:
                if rat[1] < 61:
                    self.rating[1] = "Число задолженностей у студентов:"
                    self.rating[2][key] += 1
            if self.rating[2][key] != 0:
                self.rating[0] += 1
            else:
                del self.rating[2][key]

        return self.rating
```
#### Модульные тесты, созданные для файла CalcAcademicFailure.py содержатся в файле test_CalcAcademicFailure.py внутри класса TestAcadFail.
```python
from src.Types import DataType
from src.CalcAcademicFailure import CalcAcadFail
import pytest

RatingType = list[int, str, dict[str, int]]


class TestAcadFail:
    @pytest.fixture()
    def input_data(self) -> tuple[DataType, DataType, RatingType, RatingType]:
        data_fail: DataType = {
            "Иванов Иван Иванович": [
                ("математика", 67),
                ("литература", 100),
                ("программирование", 91)
            ],
            "Петров Петр Петрович": [
                ("математика", 90),
                ("химия", 87),
                ("социология", 60)
            ]
        }
        data: DataType = {
            "Иванов Иван Иванович": [
                ("математика", 67),
                ("литература", 100),
                ("программирование", 91)
             ],
            "Петров Петр Петрович": [
                 ("математика", 78),
                 ("химия", 87),
                 ("социология", 61)
             ]
        }
        failure: RatingType = [
            1,
            'Число задолжностей у студентов:',
            {'Петров Петр Петрович': 1}]
        nofailure: RatingType = [
            0,
            'Все студенты сдали сессию !',
            {}]

        return data_fail, data, failure, nofailure

    def test_init_calc_acadfail(self, input_data: tuple[DataType,
                                                        RatingType]) -> None:
        calc_acadfail = CalcAcadFail(input_data[0])
        assert input_data[0] == calc_acadfail.data

    def test_calc_acadfail(self, input_data: tuple[DataType,
                                                   RatingType]) -> None:
        failures = CalcAcadFail(input_data[0]).calc()
        assert failures[0] == input_data[2][0]
        for student in failures[2].keys():
            fail_lot = failures[2][student]
            assert fail_lot == input_data[2][2][student]

    def test_calc_notacadfail(self, input_data: tuple[DataType,
                                                      RatingType]) -> None:
        nofail = CalcAcadFail(input_data[1]).calc()
        assert nofail == input_data[3]
```
#### Реализуем работу с новыми классами в файле main.py:
```python
import argparse
import sys

from JsonDataReader import JsonDataReader
from CalcAcademicFailure import CalcAcadFail


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
#    reader = TextDataReader()
    reader = JsonDataReader()
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcAcadFail(students).calc()
    print("Число студентов имеющих задолженность(ти): " + str(rating[0]))
    print(rating[1])
    print(rating[2])


if __name__ == "__main__":
    main()

```
#### Результат работы программы:
```
C:\anaconda3\envs\PTLab1-2022\python.exe C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\src\main.py -p ../data/data.json 
Students:  {'Иванов Иван Иванович': [('математика', 80), ('литература', 100), ('программирование', 91)], 'Петров Петр Петрович': [('математика', 60), ('химия', 87), ('социология', 75)]}
Число студентов имеющих задолженность(ти): 1
Число задолженностей у студентов:
{'Петров Петр Петрович': 1}

Process finished with exit code 0
```
#### Тестирование функции calc() класса CalcAcadFail:
```
C:\anaconda3\envs\PTLab1-2022\python.exe "C:/Users/Дмитрий/PyCharm Community Edition 2022.2.2/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py" --path C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test\test_CalcAcademicFailure.py 
Testing started at 19:37 ...
Launching pytest with arguments C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test\test_CalcAcademicFailure.py --no-header --no-summary -q in C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test

============================= test session starts =============================
collecting ... collected 3 items

test_CalcAcademicFailure.py::TestAcadFail::test_init_calc_acadfail PASSED [ 33%]
test_CalcAcademicFailure.py::TestAcadFail::test_calc_acadfail PASSED     [ 66%]
test_CalcAcademicFailure.py::TestAcadFail::test_calc_notacadfail PASSED  [100%]

============================== 3 passed in 0.03s ==============================

Process finished with exit code 0

```
#### Коммиты в ветку calc_af:
![calc_af](https://user-images.githubusercontent.com/61357719/201533301-01ef4f43-1dca-4999-bf64-195f7a198ede.png)

## Этап 3. Работа с проектом.
#### Результаты тестирования всех функций в проекте:
```
C:\anaconda3\envs\PTLab1-2022\python.exe "C:/Users/Дмитрий/PyCharm Community Edition 2022.2.2/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py" --path C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test 
Testing started at 19:40 ...
Launching pytest with arguments C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test --no-header --no-summary -q in C:\Users\Дмитрий\PycharmProjects\PTLab1-2022\test

============================= test session starts =============================
collecting ... collected 10 items

test_CalcAcademicFailure.py::TestAcadFail::test_init_calc_acadfail PASSED [ 10%]
test_CalcAcademicFailure.py::TestAcadFail::test_calc_acadfail PASSED     [ 20%]
test_CalcAcademicFailure.py::TestAcadFail::test_calc_notacadfail PASSED  [ 30%]
test_CalcRating.py::TestCalcRating::test_init_calc_rating PASSED         [ 40%]
test_CalcRating.py::TestCalcRating::test_calc PASSED                     [ 50%]
test_JsonDataReader.py::TestJsonDataReader::test_read PASSED             [ 60%]
test_JsonDataReader.py::test_noncorrect_path_to_file PASSED              [ 70%]
test_TextDataReader.py::TestTextDataReader::test_read PASSED             [ 80%]
test_main.py::test_get_path_from_correct_arguments PASSED                [ 90%]
test_main.py::test_get_path_from_noncorrect_arguments PASSED             [100%]

============================= 10 passed in 0.12s ==============================

Process finished with exit code 0

```
#### Построим UML диаграмму проекта с помощью расширения PlantUML и добавим файлы UML диаграммы в проект:
![UML](/test_UML.png)

#### После добавления файлов .gitignore и license.md структура проекта выглядит следующим образом:
![project_struct](https://user-images.githubusercontent.com/61357719/201534024-f357e8a4-e0d8-4932-bb53-0929546b1958.png)

### Используемые библиотеки:
pycodestyle

pytest

## Выводы 
1. Научился работать с системой контроля версий кода Git и ее функциями;
2. Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание»
(CD);
3. Получил навыки разработки ООП-программ и написания модульных тестов к ним на языке программирования Python;
4. Получил навыки работы с системой Git для хранения и управления версиями ПО;
5. Получил навыки управления автоматизированным тестированием программного обеспечения,
расположенного в системе Git, с помощью инструмента GitHub Actions.
