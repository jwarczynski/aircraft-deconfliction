from solver import deconflict

def read_matrix(filename):
    # Wyciągnięcie wielkości instancji z nazwy pliku
    configuration = filename.split("_")
    planes = int(configuration[0])
    maneuvers = int(configuration[1])
    # Otwarcie pliku i odczytanie zawartości
    with open("instances/"+filename, 'r') as f:
        content = f.read()

    # Konwersja zawartości na listę int'ów
    colision_matrix = []
    idx = 0
    numbers = [int(x) for x in content.split()]

    # załadowanie dancyh do macierzy kolizji 
    for manewr in range(maneuvers):
        colision_matrix.append([])
        for plane in range(planes):
            colision_matrix[manewr].append([])
            for manewr2 in range(maneuvers):
                colision_matrix[manewr][plane].append([])
                for _ in range(planes):
                    colision_matrix[manewr][plane][manewr2].append(numbers[idx])
                    idx += 1

    return colision_matrix, planes


def get_average_times(p_range, m_range, f_range, i_range):
    avg_times = []
    solutions_num = []
    for planes in p_range:
        for maneuvers in m_range:
            for filling in f_range:
                total_config_time = 0
                solutions = 0
                for instance in i_range:
                    # print(f'instance: {planes}_{maneuvers}_{filling}_{instance}')
                    cm, _ = read_matrix(f'{planes}_{maneuvers}_{filling}_{instance}')
                    model, _ = deconflict(cm, planes, maneuvers)
                    total_config_time += model.solve_details.time
                    print(f'instance {planes}_{maneuvers}_{filling}_{instance}  time: {model.solve_details.time}')
                    if model.solve_details.status in ["optimal", "feasible", "integer optimal solution"]:
                        solutions += 1
                total_config_time /= (i_range[-1] + 1)
                print(f'instance {planes}_{maneuvers}_{filling}  avg time: {total_config_time}  solutions: {solutions}')
                avg_times.append(total_config_time)
                solutions_num.append(solutions)
    
    return (avg_times, solutions_num)