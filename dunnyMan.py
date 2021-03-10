import pandas as pd
import numpy as np
import os
import shutil


class DunnyMan:
    def __init__(self):
        self.path = os.getcwd()
        self.files = os.listdir(self.path)
        os.makedirs(self.path + './.temp/', exist_ok=True)
        self.tempDir = self.path + '/.temp/'

    def setPath(self, path=None):
        if path is None:
            self.path = os.getcwd()
        else:
            self.path = path

    def setFile(self, file=None):
        if file is None:
            self.files = os.listdir(self.path)

    def getTextFile(self):
        files_txt = [f for f in self.files if f[-13:] == 'WC_Alarms.txt']

        for file in files_txt:
            with open(file) as fin, open(self.tempDir + 'WC_Alarms.csv', 'w') as fout:
                for line in fin.readlines():
                    fout.write(line.replace('\t', ','))

        tempFile = self.tempDir + '/WC_Alarms.csv'
        alarms = pd.read_csv(tempFile, sep=',',
                             names=["Time", "Mode",
                                    "Alarm01", "Alarm02", "Alarm03", "Alarm04", "Alarm05",
                                    "Alarm06", "Alarm07", "Alarm08", "Alarm09", "Alarm10"
                                    "Alarm11", "Alarm12", "Alarm13", "Alarm14", "Alarm15"])
        alarms = alarms.dropna(axis=1, how='all')

        alarms = alarms.fillna(0)

        for col in alarms.columns[2:]:
            alarms[col] = alarms[col].astype(np.int64)
        alarms.to_csv('WC_Alarms.csv')

        overTemp = alarms[(alarms == 29).any(axis=1)]

        overTemp.to_csv('OverTempLogs.csv')

    def removeTempDir(self):
        try:
            shutil.rmtree(self.tempDir)
            print(".tempDir and all of its contents has been deleted.")
        except FileNotFoundError:
            print(".tempDir does not exist")
