import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from pandas import display


def plot_times_solutions(times, solutions, instances, xlabel, title, fit_poly=False):

    fig, ax1 = plt.subplots()
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Czas rozwiązania [s]')
    ax1.plot(instances, times, 'o-', color='tab:orange', alpha=0.5, label='Czas rozwiązania')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Liczba rozwiązań')
    ax2.plot(instances, solutions, "s-", color='tab:blue', label='Liczba rozwiązań')
    ax2.tick_params(axis='y')

    # Dopasowanie liniowe po zlogarytmowaniu wartości
    mask = times != 0
    coef1 = np.polynomial.polynomial.polyfit(instances[mask], np.log(times[mask]), 1)
    p1 = np.polynomial.Polynomial(coef1)
    a1 = np.exp(p1.coef[0])
    b1 = p1.coef[1]
    x_fitted1 = np.linspace(np.min(instances), np.max(instances), 100)
    y_fit1 = a1 * np.exp(b1 * x_fitted1)

    # Dopasowanie wielomianu 2 stopnia
    deg = 2
    coef2 = np.polynomial.polynomial.polyfit(instances, times, deg)
    p2 = np.polynomial.Polynomial(coef2)
    y_fit2 = p2(x_fitted1)

    # Wzory w LaTeX
    formula1 = rf"${a1:.6f}\cdot e^{{{b1:.2f}x}}$"
    # formula2 = rf"${p2.coef[0]:.3f} + {p2.coef[1]:.3f}\cdot x$"
    formula2 = rf"${p2.coef[0]:.3f} + {p2.coef[1]:.3f}\cdot x + {p2.coef[2]:.3f}\cdot x^{2}$"
    # formula2 = rf"${p2.coef[0]:.3f} + {p2.coef[1]:.3f}\cdot x + {p2.coef[2]:.3f}\cdot x^{2} + {p2.coef[3]:.3f}\cdot x^{3}$"

    # ax1.plot(x_fitted1, y_fit1, color='tab:green', label=f'Dopasowanie eksponencjalne: {formula1}')
    if fit_poly:
        ax1.plot(x_fitted1, y_fit2, color='tab:green', label=f'Dopasowanie wielomianowe: {formula2}')

    # Ustawienie legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines = lines1 + lines2
    labels = labels1 + labels2
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.2))

    ax1.set_title(title)

    # Wyświetlenie wykresu
    fig.tight_layout()
    plt.show()

def show_plot(path, xlabel, title, x, col_index, fit_poly=False):
    data = np.genfromtxt(path, delimiter=',', skip_header=1)
    times = data[:, 0]
    sol = data[:, 1]

    plot_times_solutions(times, sol, x, xlabel, title, fit_poly)

    data = {col_index: x, 'Średni czas roziwązania': times, 'Liczba rozwiązań': sol}
    show_table(data, col_index)

    
def show_planes_plot():
    sizes = np.linspace(10, 150, 15)
    title = "czas rozwiązania w funkcji ilości statków powietrznych"
    xlabel = "ilość statków powietrznych"
    path = "planes.csv"
    col_index = "ilość statków powietrznych "

    show_plot(path, xlabel, title, sizes, col_index, True)
    

def show_maneuvers_plot(file):
    ran =  file.split("_")[1]
    print(ran)
    s = int(ran.split("-")[0])
    e = int(ran.split("-")[1])
    if e-s > 20:
        step = 10
        sizes = np.linspace(s, e, int((e-s+10)/step))
    else:
        step = 1
        sizes = np.linspace(s, e, int((e-s)/step))
    title = "czas rozwiązania w funkcji liczby dostępnych manewrów"
    xlabel = "liczba dopuszczalnych manewrów"
    path = f"maneuvers_{file}.csv"
    file_path = os.path.join("..", "out", "basic", path)
    col_index = "liczba dopuszczalnych manewrów"

    show_plot(file_path, xlabel, title, sizes, col_index, True)

def show_density_plot():
    sizes = np.linspace(10, 38, 15)
    title = "czas rozwiązania w funkcji gęstości konfliktów"
    xlabel = "gęstość konfliktów w %"
    path = "density.csv"
    col_index = "procentowa gęstość konfliktów"

    show_plot(path, xlabel, title, sizes, col_index)

def show_density_plot2():
    sizes = np.arange(15, 25)
    title = "czas rozwiązania w funkcji gęstości konfliktów"
    xlabel = "gęstość konfliktów w %"
    path = "density2.csv"
    col_index = "procentowa gęstość konfliktów"

    show_plot(path, xlabel, title, sizes, col_index)


def show_table(data, index):
    df = pd.DataFrame(data)
    df = df.set_index(index)
    display(df)
