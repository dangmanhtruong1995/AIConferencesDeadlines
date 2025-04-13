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
from pdb import set_trace
import shutil
import pandas as pd
from pprint import pprint
import getpass
import os
from datetime import datetime
from copy import deepcopy
import atexit

from myutils import CSVFileBuilderFromData

def main():
    year = 2025
    conference_deadline_file_name = f"Conference_deadlines_{year}_according_to_AI_agent.csv"
    conference_deadline_date_only_file_name = f"Conference_deadlines_{year}_date_only_according_to_AI_agent.csv"
    conference_deadline_processed_file_name = f"Conference_deadlines_{year}_processed.csv"
    
    df = pd.read_csv(conference_deadline_date_only_file_name)
    conference_list = df["conference_name"].to_list()
    file_builder = CSVFileBuilderFromData(conference_deadline_processed_file_name)

    for index, row in df.iterrows():
        conference_name = row["conference_name"]
        date = row["date"]

        date = date.replace("0th", "0")
        date = date.replace("1th", "1")
        date = date.replace("2th", "2")
        date = date.replace("3th", "3")
        date = date.replace("4th", "4")
        date = date.replace("5th", "5")
        date = date.replace("6th", "6")
        date = date.replace("7th", "7")
        date = date.replace("8th", "8")
        date = date.replace("9th", "9")
        date = date.replace("1st", "1")
        date = date.replace("2nd", "2")
        date = date.replace("3rd", "3")

        splitted = date.split(",")
        if len(splitted) >= 3:
            date = ",".join(splitted[:2])

        date =re.sub("[\(\[].*?[\)\]]", "", date)

        file_builder.add_data(conference_name=conference_name, date=date)

    # Save the results to file
    file_builder.build_file()


if __name__ == "__main__":
    main()
