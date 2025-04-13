import pandas as pd
import numpy as np

class CSVFileBuilderFromData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = {}
        
    def add_data(self, **kwargs):
        for key, val in kwargs.items():
            if key not in self.data:
                self.data[key] = [val]
            else:
                self.data[key].append(val)

    def build_file(self):
        df = pd.DataFrame(self.data)
        df.to_csv(self.file_name, sep=',', encoding='utf-8', index=False, header=True)
        # set_trace()
        pass