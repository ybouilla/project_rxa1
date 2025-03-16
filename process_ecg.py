from typing import List, Tuple
import pandas as pd
import numpy as np
import csv

def load_ecg_file(file: str) -> pd.DataFrame:
    dataset = {'wave_type':[], 'wave_onset': [], 'wave_offset': [], 'wave_tags': []}
    with open(file, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader: 
            dataset['wave_type'].append(row[0])
            dataset['wave_onset'].append(row[1])
            dataset['wave_offset'].append(row[2])
            if len(row) > 3:
                 dataset['wave_tags'].append(row[3])
            else:
                 dataset['wave_tags'].append(None)

    dataset = pd.DataFrame.from_dict(dataset)
    return dataset


def compute_heart_cycle_duration(dataset: pd.DataFrame) -> Tuple[np.ndarray, pd.DataFrame]:
     """
     Returns a serie with the heart cycle duration for each detected cycle
     """
     df= dataset[dataset['wave_type'] == 'QRS']
     df['QRS_peek'] = (df['wave_offset'].astype('int32') - df['wave_onset'].astype('int32'))*.5 + df['wave_offset'].astype('int32')
     # df['cycle_time_1'] = df['wave_onset']
     # df['cycle_time_2'] = df['wave_offset']
     # df['wave_onset'] = df['wave_onset'].astype('int32')
     # df['wave_offset'] = df['wave_offset'].astype('int32')
     #time_elapsed_1 = df['wave_onset'].tail(1).iat[0] - df['wave_onset'].head(1).iat[0]

     df = df.reset_index()

     _wave_onset = df['wave_onset'].to_numpy()
     _wave_offset = df['wave_offset'].to_numpy()
     cycle_time = np.zeros((len(df)-1,))
     for i in range(len(df)-1):
          cycle_time[i] = _wave_onset[i+1] - _wave_onset[i]
          # df.at[i, 'cycle_time_1'] = df.at[i+1, 'wave_onset'] - df.at[i, 'wave_onset']
          # df.at[i, 'cycle_time_2'] = df.at[i+1, 'wave_offset'] - df.at[i, 'wave_offset']

     # mean_1 = df.iloc[:-1, :]['cycle_time_1'].mean()  

     # bpm = mean_1 * 60/1000
     # print(mean_1, df.iloc[:-1, :]['cycle_time_2'].mean(), )
     return cycle_time, df


def _convert_cycle_2_bpm(cycle: float) -> float:
     return np.round(60*1000 / cycle, 1)

def compute_mean_heart_rate(cycles: np.array) -> float:
     """
     Returns mean heart rate in bpm: beat per minutes
     """
     #mean_1 = dataset.iloc[:-1, :]['cycle_time_1'].mean()
     mean_1 = np.mean(cycles)
     return float(_convert_cycle_2_bpm(mean_1))


def compute_max_heart_rate(cycles: np.ndarray, df: pd.DataFrame) -> Tuple[float, int, int]:
     """
     Returns min heart rate of a collection of cycle
     """
     #min_cycle = dataset.iloc[:-1, :]['cycle_time_1'].min()
     min_cycle = np.min(cycles)
     idx_min_cycle = np.argmin(cycles)
     
     return float(_convert_cycle_2_bpm(min_cycle)), float(df.at[idx_min_cycle, 'wave_onset']), float(df.at[idx_min_cycle+1, 'wave_onset'])

def compute_min_heart_rate(cycles: np.ndarray, df: pd.DataFrame) -> float:
     """
     Returns max heart rate of a serie of cycle
     """
     #max_cycle = dataset.iloc[:-1, :]['cycle_time_1'].max()
     max_cycle = np.max(cycles)
     idx_max_cycle = np.argmax(cycles)
     
     return float(_convert_cycle_2_bpm(max_cycle)), float(df.at[idx_max_cycle, 'wave_onset']), float(df.at[idx_max_cycle+1, 'wave_onset'])


def process_ecg(file: str) -> List:
     """
     Computes and returns mean heart rate, minimum and maximum heart rate (in bpm)
     """
     dataset = load_ecg_file(file)
     cycles, df = compute_heart_cycle_duration(dataset)

     mean_cycle_rate = compute_mean_heart_rate(cycles)
     min_cycle = compute_min_heart_rate(cycles, df)
     max_cycle = compute_max_heart_rate(cycles, df)
     return [mean_cycle_rate, min_cycle, max_cycle]

