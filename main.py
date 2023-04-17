from helper import process_competition, pack_results_as_table

compatitors = 'assignment_data/competitors2.json'
results = 'assignment_data/results_RUN.txt'


if __name__ == '__main__':
    results_table = process_competition(compatitors_data_file=compatitors, results_data_file=results)
    print(results_table)

    # print(f'\n or as table: \n\n')
    # print(pack_results_as_table(results_table))
