import pandas as pd
import numpy as np
import os
import shutil

"""
Ben McGuffog. Project Support Engineer
Processes the WC_Alarms.txt data into a usable csv format called WC_Alarms.csv.
Filters out the Over-temperature faults and writes them to the file OverTempLogs.csv
Version 1.0
"""


class DunnyMan:
    def __init__(self):
        self.path = os.getcwd()
        self.files = os.listdir(self.path)
        self.tempDir = self.path + '/.temp/'

    def setPath(self, path=None):
        """
        Setter for the self.path var
        :param path: str
        :return: None
        """
        if path is None:
            self.path = os.getcwd()
        else:
            self.path = path

    def setFiles(self, file=None):
        """
        Setter for the self.sfiles var
        :param file: str
        :return: None
        """
        if file is None:
            self.files = os.listdir(self.path)

    def createTempPath(self, path=None):
        """
        Creates a temporary working directory called .tempDir
        :param path: str
        :return: None
        """
        self.setPath(path)
        os.makedirs(self.path + './.temp/', exist_ok=True)

    def createTempFile(self):
        """
        Grabs a file ending in 'WC_Alarms.txt' and creates a csv copy in .tempDir
        :return: None
        """
        self.setFiles()
        files_txt = [f for f in self.files if f[-13:] == 'WC_Alarms.txt']

        for file in files_txt:
            with open(file) as fin, open(self.tempDir + 'WC_Alarms.csv', 'w') as fout:
                for line in fin.readlines():
                    fout.write(line.replace('\t', ','))

    def writeCSVFile(self, df: pd.DataFrame, name: str):
        """
        Writes a pandas data frame to a csv file
        :param df: pandas DataFrame
        :param name: str
        :return: None
        """
        try:
            df.to_csv(name)
        except:
            print("Huston, we have a problem")

    def filterTempFile(self):
        """
        Separates the txt file data into a usable pandas data frame.
        :return: pandas DataFrame
        """
        try:
            tempFile = self.tempDir + '/WC_Alarms.csv'
        except FileNotFoundError:
            print("File does not exist. Exiting")
            return -1

        alarms = pd.read_csv(tempFile, sep=',',
                             names=["Time", "Mode",
                                    "Alarm01", "Alarm02", "Alarm03", "Alarm04", "Alarm05",
                                    "Alarm06", "Alarm07", "Alarm08", "Alarm09", "Alarm10"
                                    "Alarm11", "Alarm12", "Alarm13", "Alarm14", "Alarm15"])
        alarms = alarms.dropna(axis=1, how='all')

        return alarms.fillna(0)

    def convertAlarmColsToInt64(self, alarms):
        """
        Converts the Alarm columns into an int64 type.
        :param alarms: str
        :return: None
        """
        for col in alarms.columns[2:]:
            alarms[col] = alarms[col].astype(np.int64)
        self.writeCSVFile(alarms, 'WC_Alarms.csv')
        overTemp = alarms[(alarms == 29).any(axis=1)]
        self.writeCSVFile(overTemp, 'OverTempLogs.csv')

    def removeTempDir(self):
        """
        Removes the temporary working directory .tempDir
        :return:
        """
        try:
            shutil.rmtree(self.tempDir)
            print(".tempDir and all of its contents has been deleted.")
        except FileNotFoundError:
            print(".tempDir does not exist")


def main():
    dm = DunnyMan()
    dm.createTempPath()
    dm.createTempFile()
    dm.convertAlarmColsToInt64(dm.filterTempFile())
    dm.removeTempDir()


if __name__ == "__main__":
    main()