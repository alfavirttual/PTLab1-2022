# -*- coding: utf-8 -*-
import argparse
import sys

from CalcRating import CalcRating
from TextDataReader import TextDataReader


def get_path_from_arguments() -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args()
    return args.path


def main():
    path = get_path_from_arguments() # Открываем файл и записываем содержимое в path

    reader = TextDataReader()        # Конструктор класса TextDataReader
    students = reader.read(path)     # Записываем в student словарь построенный на основе path
    print("Students: ", students)    # Выводим в консоль получившийся словарь
    rating = CalcRating(students).calc() # Содаём конструктор класса CalcRating
                                         # передаём ему словарь students
                                         # в функции calc считаем срений бал

    print("Rating: ", rating)            # Печатаем словарь с рейтингом студентов


if __name__ == "__main__":
    main()
