import os
from os.path import join as pjoin
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from pdb import set_trace
from datetime import datetime
from copy import deepcopy
import re
from pathlib import Path
import getpass
import os
import shutil
import pandas as pd
from pprint import pprint
import os
from datetime import datetime
from copy import deepcopy
import atexit
import matplotlib.dates as mdates
import matplotlib
from datetime import date
import datetime as dt

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)


def is_feature(release):
    """Return whether a version (split into components) is a feature release."""
    return release[-1] == '0'


def plot_timeline(dates, releases, year):
    levels = []
    macro_meso_releases = sorted({release[:2] for release in releases})
    for idx1, release in enumerate(releases):
        level = idx1+1
        levels.append(level)

    # The figure and the axes.
    # fig, ax = plt.subplots(figsize=(8.8, 4), layout="constrained")
    fig, ax = plt.subplots(figsize=(15, 10), layout="constrained")
    # ax.set(title="Conference deadlines (full paper submission)")

    # The vertical stems.
    ax.vlines(dates, 0, levels,
            color=[("tab:red", 1 if is_feature(release) else .5) for release in releases])
    # The baseline.
    ax.axhline(0, c="black")
    # The markers on the baseline.
    meso_dates = [date for date, release in zip(dates, releases) if is_feature(release)]
    micro_dates = [date for date, release in zip(dates, releases)
                if not is_feature(release)]
    ax.plot(micro_dates, np.zeros_like(micro_dates), "ko", mfc="white")
    ax.plot(meso_dates, np.zeros_like(meso_dates), "ko", mfc="tab:red")

    # Annotate the lines.
    for date, level, release in zip(dates, levels, releases):        
        version_str = ''.join(release)
        ax.annotate(version_str, xy=(date, level),
                    xytext=(-3, np.sign(level)*3), textcoords="offset points",
                    verticalalignment="bottom" if level > 0 else "top",
                    weight="bold" if is_feature(release) else "normal",
                    bbox=dict(boxstyle='square', pad=0, lw=0, fc=(1, 1, 1, 0.7)))

    ax.xaxis.set(
        # major_locator=mdates.YearLocator(),
        #major_formatter=mdates.DateFormatter("%Y"),
        # major_locator=mdates.MonthLocator(),
        # major_formatter=mdates.DateFormatter("%M-%Y"),
    )

    # Remove the y-axis and some spines.
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    plt.show()
    plt.get_current_fig_manager().full_screen_toggle() # toggle fullscreen mode
    plt.savefig(f"AI_conference_deadlines_{year}.png")

def main():
    year = 2025
    conference_deadline_file_name = f"Conference_deadlines_{year}_according_to_AI_agent.csv"
    conference_deadline_date_only_file_name = f"Conference_deadlines_{year}_date_only_according_to_AI_agent.csv"
    conference_deadline_processed_file_name = f"Conference_deadlines_{year}_processed.csv"

    df = pd.read_csv(conference_deadline_processed_file_name)
    # df.loc[-1] = ["Current date", dt.datetime.now()]
    df['date'] = pd.to_datetime(df['date'], format="mixed")

    df = df.sort_values('date', ascending=True)
    dates = df['date'].dt.strftime('%d-%m-%Y')
    dates = dates.to_list()    

    conference_list = df['conference_name'].to_list()
    conference_list_with_dates = []
    for date, conference_name in zip(dates, conference_list):
        conference_name_with_date = f"{conference_name} ({date})"
        conference_list_with_dates.append(conference_name_with_date)
   
    # fig = plt.figure()
    plot_timeline(df['date'] , conference_list_with_dates, year)


if __name__ == "__main__":
    main()
