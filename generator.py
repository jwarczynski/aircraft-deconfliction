import numpy as np

def generate_conflict_matrix(planes, maneuvers, fill):
    num_entries = planes* maneuvers
    num_ones = int(num_entries * (num_entries - 1) / 2 * fill / 100)
    indices = np.random.choice(num_entries * (num_entries - 1) // 2, size=num_ones, replace=False)
    matrix = np.zeros((num_entries, num_entries))
    matrix[np.triu_indices(num_entries, 1)[0][indices], np.triu_indices(num_entries, 1)[1][indices]] = 1
    matrix = matrix + matrix.T
    return matrix


def save_instance_to_file(instance, filename):
    instance = instance.astype(int)
    with open(filename, 'w') as f:
        for row in instance:
            f.write(' '.join(map("{:.0f}".format, row)) + '\n')


def generate_instances(*ranges):
    for plane in ranges[0]:
        for maneuver in ranges[1]:
            for density in ranges[2]:
                for instance in ranges[3]:
                    conflict_matrix = generate_conflict_matrix(plane, maneuver, density)
                    filename = f'instances/{plane}_{maneuver}_{density}_{instance}'
                    save_instance_to_file(conflict_matrix, filename)


INSTANCES_RANGE = range(10)

# function of planes 
PLANES_RANGE_P = range(10, 160, 10)
MANEUVERS_RANGE_P = range(10,11)
DENSITY_RANGE_P = range(5, 6)
CONFIG_P = (PLANES_RANGE_P, MANEUVERS_RANGE_P, MANEUVERS_RANGE_P, INSTANCES_RANGE)

# function of maneuvers
MANEUVERS_RANGE_M = range(10,160,10)
PLANES_RANGE_M = range(20, 21)
DENSITY_RANGE_M = range(5, 6)
CONFIG_M = (PLANES_RANGE_M, MANEUVERS_RANGE_M, MANEUVERS_RANGE_M, INSTANCES_RANGE)

# function of density
DENSITY_RANGE_D = range(15, 25, 1)
PLANES_RANGE_D = range(20, 21)
MANEUVERS_RANGE_D = range(10,11)
CONFIG_D = (PLANES_RANGE_D, MANEUVERS_RANGE_D, DENSITY_RANGE_D, INSTANCES_RANGE)

generate_instances(*CONFIG_D)