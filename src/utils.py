from solver import deconflict
import os


def read_matrix(filename):
    # Wyciągnięcie wielkości instancji z nazwy pliku
    configuration = filename.split("_")
    planes = int(configuration[0])
    maneuvers = int(configuration[1])
    # Otwarcie pliku i odczytanie zawartości
    file_path = os.path.join("..", "instances", filename)
    with open(file_path, 'r') as f:
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


def get_average_times(p_range, m_range, f_range, i_range, optimize=False):
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
                    model, _ = deconflict(cm, planes, maneuvers, optimize)
                    total_config_time += model.solve_details.time
                    print(f'instance {planes}_{maneuvers}_{filling}_{instance}  time: {model.solve_details.time}    status: {model.solve_details.status}')
                    if model.solve_details.status in ["optimal", "feasible", "integer optimal solution"]:
                        solutions += 1
                total_config_time /= (i_range[-1] + 1)
                print(f'instance {planes}_{maneuvers}_{filling}  avg time: {total_config_time}  solutions: {solutions}')
                avg_times.append(total_config_time)
                solutions_num.append(solutions)
    
    return (avg_times, solutions_num)

def get_times_and_solutions(p_range, m_range, f_range, i_range, optimize=False):
    times = []
    statuses = []
    solutions = []
    instances = []
    iters = []
    for planes in p_range:
        for maneuvers in m_range:
            for filling in f_range:
                total_config_time = 0
                sol_num = 0
                for instance in i_range:
                    cm, _ = read_matrix(f'{planes}_{maneuvers}_{filling}_{instance}')
                    model, _ = deconflict(cm, planes, maneuvers, optimize)

                    total_config_time += model.solve_details.time
                    
                    print(f'instance {planes}_{maneuvers}_{filling}_{instance}  time: {model.solve_details.time}    status: {model.solve_details.status}')
                    iters.append(instance)
                    instances.append(f'{planes}_{maneuvers}_{filling}_{instance}')
                    statuses.append(model.solve_details.status)
                    if model.solve_details.status in ["optimal", "feasible", "integer optimal solution"]:
                        solutions.append(1)
                        sol_num +=1
                    else:
                        solutions.append(0)
                    times.append(model.solve_details.time)

                total_config_time /= (i_range[-1] + 1)
                print(f'instance {planes}_{maneuvers}_{filling}  avg time: {total_config_time}  solutions: {sol_num}')
    return (iters, instances, times, solutions, statuses)


if __name__ == "__main__":
    pass
