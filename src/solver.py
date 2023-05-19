from docplex.mp.model import Model


def deconflict(cm, planes_num, maneuvers):
    # Tworzenie modelu
    model = Model(name='Binary variables model')

    # Zmienne decyzyjne
    x = {(i,j): model.binary_var(name='x_{0}_{1}'.format(i,j)) for i in range(0,planes_num) for j in range(0, maneuvers)}

    # Ograniczenia
    # Pierwsze ograniczenie
    for i in range(0,planes_num):
        model.add_constraint(model.sum(x[(i,j)] for j in range(0,maneuvers)) == 1)

    # Drugie ograniczenie
    for i in range(0, planes_num):
        for j in range(0, maneuvers):
            for k in range(i+1, planes_num):
                for l in range(0, maneuvers):
                    model.add_constraint(x[(i,j)]*cm[j][i][l][k] + x[(k,l)]*cm[j][i][l][k] <= 1)
                    

    # Rozwiązanie problemu
    model.solve()

    return model, x


if __name__ == "__main__":
    pass
