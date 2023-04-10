from helper import get_runners_data, pack_runners_data, get_results
import os


compatitors = 'assignment_data/competitors2.json'
results = 'assignment_data/results_RUN.txt'


if __name__ == '__main__':
    print("hello!")

    # print(path)
    runners = pack_runners_data(get_runners_data(compatitors))

    for runner in runners:
        print(runner)

    print(get_results(results))

    # print