"""
    В этом модуле реализованы функции, которые парсят данные, 
    обрабатывают и выдают в нужном виде.

    Создаем Дата-класс `Runner` - хранит имя и фамилию бегуна

    Функции `_get_runners_data` и `_get_results_data` читают данные из файлов.

    Далее данные поступают в функции обработчики.

    `_pack_runners_data` упаковывается данные о бегунах в словарь, 
    в котором нагрудный номер - это ключ, значение - экземпляр дата-класса Runner. возвращает словарь. 
    Было решено упаковать в словарь, т.к. проще получить данные о бегуне при создании конечного списка.
    С дата классом типа именованного кортожеа просто удобнее работать.

    `_process_results` - обрабатывает результаты - рассчитывает время бега, 
    сортирует бегунов по времени и возвращается отсортированный список

    функция `_make_final_output` получается словарь бегунов и массив результатов, собирает все в конечный словарь
    в формате << | место | нагрудный номер | имя | фамилия | время | >>
"""

import json 
import io
from typing import NamedTuple
import datetime

class Runner(NamedTuple):
    name: str
    surname: str


    def __str__(self) -> str:
        return f'{self.name} {self.surname} with number {self.id}'


def _get_runners_data(file: str) -> dict:
    """ Читает файл в формате json, который хранит информацию о спортсменах.
    возвращает словарь.

    применяется кодировка 'utf-8-sig', чтобы нормально обработать BOM.
    """
    with io.open(file, encoding='utf-8-sig', mode='r') as json_file:
        runners_data = json.load(json_file)

    return runners_data


def _pack_runners_data(data: dict) -> 'dict[str, Runner]':
    """Обрабатываем прочитанные данные из json файла.
    Удаляем BOM = '\ufeff' из значений ключей.

    Данные о спортсменах упаковываем в дата-класс Runner.
    Все упаковывем в словарь: ключ - нагрудный номер, значение - Runner
    """
    runners = dict()
    keys = data.keys()
    for key in keys:
        compatitor = data[key]
        if '\ufeff' in str(key):
            id = int(str(key).replace('\ufeff', ''))
        else:
            id = int(key)
        runners[str(id)] = Runner(name=compatitor['Name'], surname=compatitor['Surname'])

    return runners


def _get_results_data(file: str) -> list:
    """Читаем построчно текстовый файл и разделяем данные в список
    """
    with io.open(file, encoding='utf-8-sig', mode='r') as file:
        results = file.readlines()

    results_data = []
    for line in results:
        results_data.append(line.split(sep=' '))

    return results_data


def _process_results(results: list) -> list:

    deltas = []

    for i in range(0, len(results), 2):

        start = results[i][2][:len(results[i][2])-1]
        finish = results[i+1][2][:len(results[i+1][2])-1]

        start = datetime.datetime.strptime(start, '%H:%M:%S,%f')
        finish = datetime.datetime.strptime(finish, '%H:%M:%S,%f')

        delta = finish - start
        micro = int(delta.microseconds / 10**4)

        delta = (datetime.datetime.min + delta).time()

        res = f'{delta.strftime("%M:%S")},{micro}'

        deltas.append([results[i][0], res, delta])

    deltas.sort(key= lambda x: x[2])

    return deltas


def _make_final_output(results: list, runners: 'dict[str, Runner]') -> list:

    # место--id--имя--фамилия-время

    output = []
    for i in range(len(results)):
        runner = runners[results[i][0]]
        output.append([i+1, results[i][0], runner.name, runner.surname, results[i][1]])

    return output


def process_competition(compatitors_data_file: str, results_data_file: str) -> list:
    runners = _get_runners_data(compatitors_data_file)
    runners = _pack_runners_data(runners)
    results = _get_results_data(results_data_file)
    results = _process_results(results)
    output = _make_final_output(results=results, runners=runners)

    return output


def pack_results_as_table(results) -> list:
    output = '| Занятое место | Нагрудный номер | Имя | Фамилия | Результат |\n'
    output +='| --- | --- | --- | --- | --- |\n'
    for result in results:
        output += f'| {result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4]} |\n'

    return output
