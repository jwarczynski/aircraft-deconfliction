import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def get_df(filename):
    path = os.path.join("..", "out", "extended", filename)
    return pd.read_csv(path)


def add_mean_times(df):
    df['InstancePrefix'] = df['instance'].str.split('_').str[:-1].str.join('_')
    df['MeanTime'] = df.groupby('InstancePrefix')['time'].transform('mean')
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
    ax.set_xticks(ind + width / 2)
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

    set_plot_description(ax, ind, width, xticks, xlabel, title)    
    plt.show()

def getType(first_letter):
    if first_letter == "p":
        return 0
    if first_letter == "m":
        return 1
    if first_letter == "d":
        return 2

def generate_bar_chart(filename, xlabel="", title=""):
    df = get_df(filename)
    add_mean_times(df)
    type = getType(filename[0])
    
    df_solution_0, df_solution_1 = fill_missing(df)
    mean_times_solution_0, mean_times_solution_1 = get_avg_times_by_instance_and_status(df_solution_0, df_solution_1)
    xticks = [x.split('_')[type] for x in df['InstancePrefix'].unique()]
    show_bar_plot(mean_times_solution_0, mean_times_solution_1, xticks, xlabel, title)
