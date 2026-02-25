import pandas as pd


# Do stuff with the data
class DataHandler():
    def __init__(self, csv_path):
        """ Initialize the data handler with the data

        Args:
            csv_path (str): the path to the data as a csv file
        """
        self.__df = pd.read_csv(csv_path)

