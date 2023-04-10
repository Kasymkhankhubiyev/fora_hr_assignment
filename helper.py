"""
    В этом модуле реализованы функции, которые парсят данные, 
    обрабатывают и выдают в нужном виде.
"""

import json 
import io
from typing import NamedTuple


class Runner(NamedTuple):
    id: str
    name: str
    surname: str


    def __str__(self) -> str:
        return f'{self.name} {self.surname} with number {self.id}'


def get_runners_data(file: str) -> dict:
    with io.open(file, encoding='utf-8-sig', mode='r') as json_file:
        runners_data = json.load(json_file)

    return runners_data


def pack_runners_data(data: dict) -> 'list[Runner]':
    runners = []
    keys = data.keys()
    for key in keys:
        compatitor = data[key]
        if '\ufeff' in str(key):
            id = int(str(key).replace('\ufeff', ''))
        else:
            id = int(key)
        runners.append(Runner(id=id, name=compatitor['Name'], surname=compatitor['Surname']))

    return runners


def get_results(file: str):
    with io.open(file, encoding='utf-8-sig', mode='r') as file:
        results = file.readlines()

    results_data = []
    for line in results:
        results_data.append(line.split(sep=' '))

    return results_data
