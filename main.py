from pyannote.audio import Pipeline, Audio

import pandas as pd

def pyannote_diarization(my_wav):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")

    # 4. apply pretrained pipeline
    diarization = pipeline(my_wav)

    # 5. print the result and save to arr
    times = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        times.append((round(turn.start, 1), round(turn.end, 1), speaker))
    return times

    # for row in excel, find time of dirarization
    # find which speaker the coordinates of y62-y66 or x somehow are changed in that time
    # for the whole range of sampling, the speaker is the one which has the larger movement

def smoothing(diarization):
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        times = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            if times[-1] == speaker:
                times[-1] = ((times[-1][0], round(turn.end, 1), speaker))
            else:
                times.append((round(turn.start, 1), round(turn.end, 1), speaker))
        print(times)
        return times


def excel_diarization(times, excel_path):
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


def compare_outputs(out1, out2):
    for i in range(len(out1)):
        if out1[i][2] == out2[i][2]:
            print("conflict at i ", i, out1[i][0])
    print("finished loop")


def run_s_i(csv1, wav1):
    time_speaker = pyannote_diarization(wav1)
    final_out1 = excel_diarization(time_speaker, csv1)
    print(final_out1)
    return final_out1


if __name__ == '__main__':
    csv2 = 'data/220_EMO_I.csv'
    wav2 = "data/220_EMO_I.wav"
    out2 = run_s_i(csv2, wav2)

    csv1 = 'data/220_EMO_S.csv'
    wav1 = "data/220_EMO_S.wav"
    out1 = run_s_i(csv1, wav1)

    compare_outputs(out1, out2)



    # time_speaker = pyannote_diarization("data/220_EMO_S.wav")
    # #time_speaker = pyannote_diarization("data/combined_vid1.wav")
    # path = 'data/220_EMO_S.csv'

    # wav1 = "data/combined_vid1.wav"
    # csv1 = "data/test.csv"
    # run_s_i(csv1, wav1)

