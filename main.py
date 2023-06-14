from pyannote.audio import Pipeline, Audio

import pandas as pd


# from IPython.display import Audio as IPythonAudio
# from pyannote.database.util import load_rttm


# def with_ground_truth():
#     OWN_FILE = {'audio': "combined_vid1.wav"}
#
#     # load audio waveform and play it
#     waveform, sample_rate = Audio(mono="downmix")(OWN_FILE)
#     IPythonAudio(data=waveform.squeeze(), rate=sample_rate, autoplay=True)
#
#     # loading ground truth
#     groundtruths = load_rttm("groundtruth_marissa.rttm")
#     groundtruth = groundtruths[OWN_FILE['combined_vid1']]
#     print("recodnized ground truth")
#
#     pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization',
#                                         use_auth_token="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")
#
#     diarization = pipeline(OWN_FILE, groundtruth)
#
#     # 5. print the result
#     for turn, _, speaker in diarization.itertracks(yield_label=True):
#         print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
#
#     from pyannote.metrics.diarization import DiarizationErrorRate
#     metric = DiarizationErrorRate()
#     der = metric(groundtruth, diarization)
#
#     print(f'diarization error rate = {100 * der:.1f}%')
#
#
# def new_ground_truth():
#     from pyannote.database import FileFinder
#
#     # Define the path to your .rttm file
#     rttm_file = '/path/to/your/ground_truth.rttm'
#
#     # Use FileFinder to load the .rttm file
#     file_finder = FileFinder()
#     annotation = file_finder(rttm_file)
#     from pyannote.core import Segment, Annotation
#
#     # Create an empty Annotation
#     ground_truth = Annotation()
#
#     # Iterate over the lines in the .rttm file
#     with open(rttm_file, 'r') as f:
#         for line in f:
#             # Parse each line
#             _, _, _, start, duration, _, _, speaker, _, _ = line.strip().split()
#
#             # Convert the start and duration to floats
#             start = float(start)
#             duration = float(duration)
#
#             # Create a Segment for the current speaker turn
#             segment = Segment(start, start + duration)
#
#             # Add the speaker turn to the ground truth annotation
#             ground_truth[segment] = speaker

def test_anote(my_wav):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")

    # 4. apply pretrained pipeline
    diarization = pipeline(my_wav)

    # 5. print the result and save to arr
    times = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        times.append((round(turn.start, 1), round(turn.end, 1)))
    return times

    # for row in excel, find time of dirarization
    # find which speaker the coordinates of y62-y66 or x somehow are changed in that time
    # for the whole range of sampling, the speaker is the one which has the larger movement
def is_speaker(times, excel_path):
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
            if abs(y_66[i] - y_62[i]) > 1 + baseline:  # mouth open
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
    time_speaker = test_anote(wav1)
    final_out1 = is_speaker(time_speaker, csv1)
    print(final_out1)
    return final_out1


if __name__ == '__main__':
    csv1 = 'data/220_EMO_S.csv'
    wav1 = "data/220_EMO_S.wav"
    out1 = run_s_i(csv1, wav1)

    csv2 = 'data/220_EMO_I.csv'
    wav2 = "data/220_EMO_I.wav"
    out2 = run_s_i(csv2, wav2)
    compare_outputs(out1, out2)



    # time_speaker = test_anote("data/220_EMO_S.wav")
    # #time_speaker = test_anote("data/combined_vid1.wav")
    # path = 'data/220_EMO_S.csv'

    # wav1 = "data/combined_vid1.wav"
    # csv1 = "data/test.csv"
    # run_s_i(csv1, wav1)

