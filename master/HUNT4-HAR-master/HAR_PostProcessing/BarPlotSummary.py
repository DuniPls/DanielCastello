# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import os
import re

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import itertools

import Dictinaries


def create_barplot(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    subject_file = os.path.join(root_dir, filename)

    subjectid = list(map(int, re.findall('\d+', filename))).pop().__str__()
    # data = pd.read_csv(subject_file)
    data = pd.read_csv(subject_file, parse_dates=[0])
    data = data.drop('H4ID', axis=1)
    data = data.drop('weekday', axis=1)
    # data = data.drop('class', axis=1)
    # convert seconds to minutes
    data = data.set_index('date')
    data = data.divide(60)
    data = data.divide(20)
    data = data[["cycling", "running", "walking", "standing", "sitting", "lying"]]

    # avg per activity
    activty_avg = data.mean() * 60

    # avg per weekday / weekend
    weekday_act_avg = data.reset_index()
    weekday_act_avg['weekday'] = data.index.weekday

    weekday_act_avg['wkd'] = weekday_act_avg.weekday.map(Dictinaries.uke_helge_norsk)
    weekday_act_avg = weekday_act_avg.assign(active=weekday_act_avg.cycling + weekday_act_avg.running + weekday_act_avg.walking)
    weekday_act_avg = weekday_act_avg.assign(inactive=weekday_act_avg.sitting)
    weekday_act_avg = weekday_act_avg[['wkd', 'active', 'inactive']]
    desired_decimals = 2
    weekday_act_avg['active'] = weekday_act_avg['active'].apply(lambda x: round(x, desired_decimals))

    weekday_act_avg = weekday_act_avg.groupby('wkd').mean() * 60
    weekday_act_avg = weekday_act_avg.reset_index()
    #   weekday_act_avg = weekday_act_avg[['wkd','active']]

    # check if both 'på ukedager' and 'på helgedager' exits - if not create it with 0
    uke = 'på ukedager' in weekday_act_avg.wkd.values
    helg = 'på helgedager' in weekday_act_avg.wkd.values

    if not uke:
        weekday_act_avg = weekday_act_avg.append(pd.DataFrame([{'wkd': 'på ukedager', 'active': 0, 'inactive': 0}]))
    if not helg:
        weekday_act_avg = weekday_act_avg.append(pd.DataFrame([{'wkd': 'på helgedager', 'active': 0, 'inactive': 0}]))

    # add sitting time table
    weekday_sit_avg = weekday_act_avg

    # weekday_act_avg.set_index('wkd', inplace=True)
    weekday_act_avg['active'] = weekday_act_avg['active'].apply(lambda x: round(x, 1))
    weekday_act_avg['avg'] = weekday_act_avg.active.map(str) + " min"
    weekday_act_avg = weekday_act_avg[['wkd', 'avg']]

    weekday_sit_avg['inactive'] = weekday_sit_avg['inactive'].apply(lambda x: round(x, 1))
    weekday_sit_avg['avg'] = weekday_sit_avg.inactive.map(str) + " min"
    weekday_sit_avg = weekday_sit_avg[['wkd', 'avg']]

    #############################  Plotting  #############################
    colors = itertools.cycle(['forestgreen', 'forestgreen', 'forestgreen', 'lightyellow', 'lightcyan', 'skyblue'])
    activities = ['cycling', 'running', 'walking', 'standing', 'sitting', 'lying']
    bar_width = 0.3
    n_dates = len(data.index)

    fig = plt.figure(figsize=(12, 7))
    ax1 = plt.subplot2grid((3, 7), (0, 0), rowspan=2, colspan=4)

    # creating date, weekday labels
    x_lab_data = data.reset_index()
    x_lab_data['weekday'] = data.index.weekday
    x_lab_data['datestr'] = data.index.strftime('%d.%m.%y ')
    x_lab_data['final'] = x_lab_data.weekday.map(Dictinaries.weekdays_norsk)
    x_lab_data['final'] = x_lab_data['datestr'].map(str) + "\n " + x_lab_data['final']
    #x_labels = ['']
    x_labels =x_lab_data.final.values

    Bplot_Xindex = list(range(n_dates))
    bottom = [0] * n_dates

    # Bar Chart
    for activity in activities:
        ax1.bar(Bplot_Xindex, data[activity].tolist(), bar_width, color=next(colors), bottom=bottom)

        bottom = [x + y for x, y in zip(bottom, data[activity].tolist())]

    ax1.set_xlabel("")
    ax1.set_ylabel("Timer")
    ax1.set_yticks([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    ax1.set_title('Fysisk aktivitetsprofil', fontsize=12, fontweight='bold')
    ax1.set_xticks(Bplot_Xindex)
    ax1.set_xticklabels(x_labels, rotation=0)

    # creating a legend
    #bike = mpatches.Patch(color='darkorange', label='Sykle')
    active = mpatches.Patch(color='forestgreen', label='Fysisk aktivitet')
    #walk = mpatches.Patch(color='forestgreen', label='Gå')
    stand = mpatches.Patch(color='lightyellow', label='Stå')
    sit = mpatches.Patch(color='lightcyan', label='Sitte')
    ly = mpatches.Patch(color='skyblue', label='Ligge')
    plt.legend(handles=[active, stand, sit, ly], loc='lower left', bbox_to_anchor=(1, 0.65))

    ############## Making the table for Gjennomsnitt fysiks aktivitet tid per dag,
    ############## first column

    ax2 = plt.subplot2grid((3, 7), (2, 0), colspan=1)
    lightgray = (0.90, 0.90, 0.90)

    col_labels = ['Tid med\nfysisk aktivitet*']
    table_vals = [['på ukedager'],
                  ['på helgedager']]

    ax2.xaxis.set_visible(False)
    ax2.yaxis.set_visible(False)
    ax2.set_frame_on(False)
    avg_values_table = plt.table(cellText=table_vals, cellLoc='left',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(0.3, 0.3, 0.9, 0.8))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(0.9, 2)

    ############### second column
    ax3 = plt.subplot2grid((3, 7), (2, 1), colspan=1)

    col_labels = ['Gjennomsnitt\nper dag']
    table_vals = [[weekday_act_avg.values[1, 1]],
                  [weekday_act_avg.values[0, 1]]]

    avg_uke = weekday_act_avg.loc[weekday_act_avg['wkd'] == 'på ukedager'].avg.item()
    avg_helg = weekday_act_avg.loc[weekday_act_avg['wkd'] == 'på helgedager'].avg.item()
    table_vals = [[avg_uke],[avg_helg]]

    ax3.xaxis.set_visible(False)
    ax3.yaxis.set_visible(False)
    ax3.set_frame_on(False)
    avg_values_table = plt.table(cellText=table_vals, cellLoc='right',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(0, 0.3, 0.9, 0.8))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(0.9, 3)

    ############ Making the table for Gjennomsnitt sitte tid per dag,
    ############ frist column
    ax4 = plt.subplot2grid((3, 7), (2, 2), colspan=1)
    col_labels = ['Tid i sittende']
    table_vals = [['på ukedager'],
                  ['på helgedager']]

    ax4.xaxis.set_visible(False)
    ax4.yaxis.set_visible(False)
    ax4.set_frame_on(False)
    avg_values_table = plt.table(cellText=table_vals, cellLoc='left',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(0.3, 0.3, 0.9, 0.8))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(0.9, 3)

    ############## second column
    col_labels = ['Gjennomsnitt\nper dag']
    ax5 = plt.subplot2grid((3, 7), (2, 3), colspan=1)

    avg_uke = weekday_sit_avg.loc[weekday_sit_avg['wkd'] == 'på ukedager'].avg.item()
    avg_helg = weekday_sit_avg.loc[weekday_sit_avg['wkd'] == 'på helgedager'].avg.item()
    table_vals = [[avg_uke],[avg_helg]]

    ax5.xaxis.set_visible(False)
    ax5.yaxis.set_visible(False)
    ax5.set_frame_on(False)
    avg_values_table = plt.table(cellText=table_vals, cellLoc='right',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(0, 0.3, 0.9, 0.8))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        # cell.set_height(1)
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(0.9, 3)

    ########### Making the table for average time of different activities,
    ########### first column

    ax6 = plt.subplot2grid((3, 7), (1, 4), colspan=1, rowspan=2)
    col_labels = ['Aktivitet']
    table_vals = [data.cycling.mean() + data.running.mean() + data.walking.mean(), data.standing.mean(),
                  data.sitting.mean(), data.lying.mean()]
    temp = [round(x * 60, 1) for x in table_vals]
    temp_str = [str(item) + ' min' for item in temp]
    table_vals = [['Fysisk aktivitet'],
                  ['Stå'], ['Sitte'], ['Ligge']]


    ax6.xaxis.set_visible(False)
    ax6.yaxis.set_visible(False)
    ax6.set_frame_on(False)

    avg_values_table = plt.table(cellText=table_vals, cellLoc='left',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(-0.1, 0.61, 0.9, 0.6))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(1, 2)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.7)

    ############# Second column
    ax7 = plt.subplot2grid((3, 7), (1, 5), colspan=1, rowspan=2)
    col_labels = ['Gjennomsnitt\nper dag']
    table_vals = [data.cycling.mean() + data.running.mean() + data.walking.mean(), data.standing.mean(),
                  data.sitting.mean(), data.lying.mean()]
    temp = [round(x * 60, 1) for x in table_vals]
    temp_str = [str(item) + ' min' for item in temp]
    table_vals = [[temp_str[0]], [temp_str[1]], [temp_str[2]],
                  [temp_str[3]]]

    ax7.xaxis.set_visible(False)
    ax7.yaxis.set_visible(False)
    ax7.set_frame_on(False)

    avg_values_table = plt.table(cellText=table_vals, cellLoc='right',
                                 colLabels=col_labels, colColours=[lightgray] * 16,
                                 bbox=(-0.4, 0.61, 0.7, 0.6))

    table_props = avg_values_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells:
        cell.set_fontsize(9)
        cell.set_linewidth(0)

    avg_values_table.scale(1, 2)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.7)

    plt.figtext(0.09, 0.04, '* Tid med fysisk aktivitet = summen av å gå, løpe/jogge og sykle')
    fig.savefig('plots/' + subjectid + '-bar-summary.png', bbox_inches='tight', dpi=150)
    plt.close()


path = "output/71*_summary.csv"

for fname in glob.glob(path):
    create_barplot(fname)

plt.close('all')
