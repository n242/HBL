import pandas as pd
import main

class Openface:
    def __init__(self, wav):
        self.wav = wav

    def excel_diarization(self, times, excel_path):
        df = pd.read_csv(excel_path, usecols=['timestamp', 'y_66', 'y_62'], engine='python', encoding='unicode_escape')
        y_66, y_62 = df['y_66'], df['y_62']
        timestamp = df['timestamp']
        baseline = abs(y_66[1] - y_62[1])
        final = []
        j = 0
        ctr_open, ctr_close = 0, 0
        n = len(times)
        for i in range(len(y_66)):
            if timestamp[i] > times[j][1] + 1:  # we past prev speaker time
                final.append((times[j][0], times[j][1], False))
                j += 1
                if j == n:
                    print("finished, i is:", i)
                    break
            elif times[j][0] + 1 < timestamp[i] < times[j][1]:
                if abs(y_66[i] - y_62[i]) > 3 + baseline:  # mouth open
                    ctr_open += 1  # he is the speaker
                    if ctr_open >= 2 and ctr_close >= 2:
                        final.append((times[j][0], times[j][1], True))
                        j += 1
                        if j == n:
                            print("finished, i is:", i)
                            break
                elif abs(y_66[i] - y_62[i]) < 1 + baseline:  # mouth close
                    ctr_close += 1
        return final


    def compare_outputs(self, out1, out2):
        for i in range(len(out1)):
            if out1[i][2] == out2[i][2]:
                print("conflict at i ", i, out1[i][0])
        print("finished loop")


    def run_s_i(self, csv1, wav, diarization):
        self.wav = wav
        time_speaker = diarization.pyannote_diarization()
        final_out1 = self.excel_diarization(time_speaker, csv1)
        print(final_out1)
        return final_out1


    def main_openface_excel(self):


        csv2 = 'data/220_EMO_I.csv'
        wav2 = "data/220_EMO_I.wav"
        out2 = self.run_s_i(csv2, wav2)

        csv1 = 'data/220_EMO_S.csv'
        wav1 = "data/220_EMO_S.wav"
        out1 = self.run_s_i(csv1, wav1)

        self.compare_outputs(out1, out2)
        diarization = main.Diarization(self.wav1)