import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
import colorsys
import os


def get_df(filename, optimize):
    if optimize:
        path = os.path.join("..", "out", "objective", filename)
    else:
        path = os.path.join("..", "out", "extended", filename)
    return pd.read_csv(path)


def add_mean_times(df):
    df['InstancePrefix'] = df['instance'].str.split('_').str[:-1].str.join('_')
    df['MeanTime'] = df.groupby('InstancePrefix')['time'].transform('mean')
    df['SolutionsNum'] = df.groupby('InstancePrefix')['solution'].transform('sum')
    df['MeanTimeByStatus'] = df.groupby(['InstancePrefix', 'status'])['time'].transform('mean')


def fill_missing(df):
    df_unique = df.drop_duplicates(subset=['InstancePrefix', 'solution'])

    df_solution_0 = df_unique[df_unique['solution'] == 0]
    df_solution_1 = df_unique[df_unique['solution'] == 1]

    missing_instances_0 = set(df_solution_1['InstancePrefix']) - set(df_solution_0['InstancePrefix'])
    missing_instances_1 = set(df_solution_0['InstancePrefix']) - set(df_solution_1['InstancePrefix'])

    # Dodawanie brakujących wierszy dla solution=0
    for instance in missing_instances_0:
        dummy_row = pd.DataFrame({'InstancePrefix': [instance], 'solution': [0], 'MeanTime': [np.nan], 'MeanTimeByStatus': [np.nan]})
        df_solution_0 = pd.concat([df_solution_0, dummy_row])

    # Dodawanie brakujących wierszy dla solution=1
    for instance in missing_instances_1:
        dummy_row = pd.DataFrame({'InstancePrefix': [instance], 'solution': [1], 'MeanTime': [np.nan], 'MeanTimeByStatus': [np.nan]})
        df_solution_1 = pd.concat([df_solution_1, dummy_row])

    return df_solution_0, df_solution_1


def get_avg_times_by_instance_and_status(df_solution_0, df_solution_1):
    # Sortowanie ramki danych względem InstancePrefix
    df_solution_0 = df_solution_0.sort_values('InstancePrefix')
    df_solution_1 = df_solution_1.sort_values('InstancePrefix')

    # Konwersja do tablic NumPy
    mean_times_solution_0 = df_solution_0['MeanTimeByStatus'].to_numpy()
    mean_times_solution_1 = df_solution_1['MeanTimeByStatus'].to_numpy()

    return mean_times_solution_0, mean_times_solution_1


def set_plot_description(ax, ind, width, xticks, xlabel, title):
    # ax.set_xticks(ind + 1.5 * width)
    ax.set_xticklabels(xticks)

    if xlabel == "":
        xlabel = "Rozmiar instancji"    
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Średni czas rozwiązania [s]')

    if title == "":
        title = "Średnie czasy dla instancji bez oraz z rozwiązaniem"
    ax.set_title(title)
    ax.legend()


def show_bar_plot(mean_times_solution_0, mean_times_solution_1, xticks, xlabel, title=""):
    fig, ax = plt.subplots()
    width = 0.40
    ind = np.arange(len(mean_times_solution_0))

    rects1 = ax.bar(ind, mean_times_solution_0, width, label='Brak rozwiązania')
    rects2 = ax.bar(ind + width, mean_times_solution_1, width, label='Występowanie rozwiązania')

    ax.set_xticks(ind + width / 2)

    set_plot_description(ax, ind, width, xticks, xlabel, title)    
    plt.show()

def getType(first_letter):
    if first_letter == "p":
        return 0
    if first_letter == "m":
        return 1
    if first_letter == "d":
        return 2

def generate_bar_chart(filename, optimize=False, xlabel="", title=""):
    df = get_df(filename, optimize)
    add_mean_times(df)
    type = getType(filename[0])
    
    df_solution_0, df_solution_1 = fill_missing(df)
    mean_times_solution_0, mean_times_solution_1 = get_avg_times_by_instance_and_status(df_solution_0, df_solution_1)
    xticks = [x.split('_')[type] for x in df['InstancePrefix'].unique()]

    show_bar_plot(mean_times_solution_0, mean_times_solution_1, xticks, xlabel, title)

def comparison_bar_chart(filename, xlabel="", title=""):
    df = get_df(filename, False)
    add_mean_times(df)

    df_optimized = get_df(filename, True)
    add_mean_times(df_optimized)

    type = getType(filename[0])
    
    df_solution_0, df_solution_1 = fill_missing(df)
    df_solution_opt_0, df_solution_opt_1 = fill_missing(df_optimized)

    mean_times_solution_0, mean_times_solution_1 = get_avg_times_by_instance_and_status(df_solution_0, df_solution_1)
    mean_times_solution_opt_0, mean_times_solution_opt_1 = get_avg_times_by_instance_and_status(df_solution_opt_0, df_solution_opt_1)
    xticks = [x.split('_')[type] for x in df['InstancePrefix'].unique()]
    show_comparison_bar_chart(mean_times_solution_0, mean_times_solution_1, mean_times_solution_opt_0, mean_times_solution_opt_1, xticks, xlabel, title)

def show_comparison_bar_chart(y0, y1, y0_opt, y1_opt, xticks, xlabel, title=""):
    fig, ax = plt.subplots(figsize=(10, 6))  # Zmiana rozmiaru wykresu
    width = 0.20
    ind = np.arange(len(y0))

     # Wybór nazwanych kolorów
    color1 = colors.CSS4_COLORS['darkred']
    color2 = colors.CSS4_COLORS['salmon']
    color3 = colors.CSS4_COLORS['teal']
    color4 = colors.CSS4_COLORS['skyblue']

    rects1 = ax.bar(ind, y0, width, label='Brak rozwiązania, brak f.celu', color=color1)
    rects2 = ax.bar(ind + width, y1, width, label='Występowanie rozwiązania, brak f.celu', color=color2)
    rects3 = ax.bar(ind + 2 * width, y0_opt, width, label='Brak rozwiązania, określona f celu', color=color3)
    rects4 = ax.bar(ind + 3 * width, y1_opt, width, label='Występowanie rozwiązania, okreslona f. celu', color=color4)

    ax.set_xticks(ind + 1.5 * width)

    set_plot_description(ax, ind, width, xticks, xlabel, title)    
    plt.show()


def avg_times_and_sols_num(filename):
    type = getType(filename[0])

    df = get_df(filename, False)
    add_mean_times(df)

    df_optimized = get_df(filename, True)
    add_mean_times(df_optimized)

    df = df.drop_duplicates(subset=['InstancePrefix'])
    df_optimized = df_optimized.drop_duplicates(subset=['InstancePrefix'])

    mean_times = df['MeanTimeByStatus'].to_numpy()
    mean_times_opt = df_optimized['MeanTimeByStatus'].to_numpy()

    sols = df['SolutionsNum'].to_numpy()
    sols_opt = df_optimized['SolutionsNum'].to_numpy()

    xticks = np.array([int(x.split('_')[type]) for x in df['InstancePrefix'].unique()])
    ind = np.arange(len(sols))


    plot_times_solutions(mean_times, mean_times_opt, sols, xticks, "romiar instancji", "czas rozwiązania w funkcji wielkości instancji", fit_poly=False)


def plot_times_solutions(mean_times, mean_times_opt, sols, instances, xlabel, title, fit_poly=False):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Czas rozwiązania [s]')
    ax1.plot(instances, mean_times, 'o-', color='tab:orange', alpha=0.5, label='Czas rozwiązania (bez funckji celu)')
    ax1.plot(instances, mean_times_opt, 'o-', color='tab:green', alpha=0.5, label='Czas rozwiązania (z funkcją celu)')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Liczba rozwiązań')
    ax2.plot(instances, sols, "s-", color='tab:blue', label='Liczba rozwiązań')
    ax2.tick_params(axis='y')

    # Dopasowanie liniowe po zlogarytmowaniu wartości
    mask = mean_times != 0
    coef1 = np.polynomial.polynomial.polyfit(instances[mask], np.log(mean_times[mask]), 1)
    p1 = np.polynomial.Polynomial(coef1)
    a1 = np.exp(p1.coef[0])
    b1 = p1.coef[1]
    x_fitted1 = np.linspace(np.min(instances), np.max(instances), 100)
    y_fit1 = a1 * np.exp(b1 * x_fitted1)

    # Dopasowanie wielomianu 2 stopnia
    deg = 2
    coef2 = np.polynomial.polynomial.polyfit(instances, mean_times, deg)
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

    # Ustawienie podziałki na osi x
    # ax1.set_xticks(np.arange(len(instances)))
    # ax1.set_xticklabels(instances)

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
