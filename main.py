from pyannote.audio import Pipeline, Audio

import pandas as pd

from IPython.display import Audio as IPythonAudio
from pyannote.database.util import load_rttm



def with_ground_truth():
    OWN_FILE = {'audio': "combined_vid1.wav"}

    # load audio waveform and play it
    waveform, sample_rate = Audio(mono="downmix")(OWN_FILE)
    IPythonAudio(data=waveform.squeeze(), rate=sample_rate, autoplay=True)

    # loading ground truth
    groundtruths = load_rttm("groundtruth_marissa.rttm")
    groundtruth = groundtruths[OWN_FILE['combined_vid1']]
    print("recodnized ground truth")

    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization',
                                        use_auth_token="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")

    diarization = pipeline(OWN_FILE, groundtruth)

    # 5. print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

    from pyannote.metrics.diarization import DiarizationErrorRate
    metric = DiarizationErrorRate()
    der = metric(groundtruth, diarization)

    print(f'diarization error rate = {100 * der:.1f}%')


def new_ground_truth():
    from pyannote.database import FileFinder

    # Define the path to your .rttm file
    rttm_file = '/path/to/your/ground_truth.rttm'

    # Use FileFinder to load the .rttm file
    file_finder = FileFinder()
    annotation = file_finder(rttm_file)
    from pyannote.core import Segment, Annotation

    # Create an empty Annotation
    ground_truth = Annotation()

    # Iterate over the lines in the .rttm file
    with open(rttm_file, 'r') as f:
        for line in f:
            # Parse each line
            _, _, _, start, duration, _, _, speaker, _, _ = line.strip().split()

            # Convert the start and duration to floats
            start = float(start)
            duration = float(duration)

            # Create a Segment for the current speaker turn
            segment = Segment(start, start + duration)

            # Add the speaker turn to the ground truth annotation
            ground_truth[segment] = speaker


def test_anote(my_wav):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")

    # 4. apply pretrained pipeline
    diarization = pipeline(my_wav)

    # 5. print the result and save to arr
    times = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        times.append((round(turn.start,1), round(turn.end,1)))
    return times


def is_speaker(start, stop, excel_path):
    # for row in excel, find time of dirarization (greater and smaller than)
    # find which speaker the coordinates of y62-y66 or x somehow are changed in that time
    # for the whole range of sampling
    # the speaker is the one which has the larger movement
    df = pd.read_csv(excel_path,  usecols=['timestamp','y_66', 'y_62'], engine ='python')#encoding= 'unicode_escape')
    y_66, y_62 = df['y_66'], df['y_62']
    timestamp = df['timestamp']
    baseline = abs(y_66[1]-y_62[1])
    dist = []
    for i in range(len(y_66)):
        if timestamp[i]> start and timestamp[i] < stop: # TODO: check times conversion
            #row_start = i
            if abs(y_66[i] - y_62[i]) > 1+baseline:
                return True  # he is the speaker
            #dist.append(abs(y_66[i] - y_62[i]))
        # if col[i][timestamp] < stop #we reached end
        #     row_end = imp
    # if max(dist) > 1+baseline:
    #     return True # he is the speaker
    return False

def using_visual_data(times, path):
    final = [] # has tuple of speaker and start, stop
    for j in range(len(times)):
        final.append((is_speaker(times[j][0]*60, times[j][1]*60, path), times[j]))

    return final


if __name__ == '__main__':
    #with_ground_truth()
    time_speaker = test_anote("data/220_EMO_S.wav")
    #time_speaker = test_anote("combined_vid1.wav")
    path = 'data/220_EMO_S.csv'
    #path = "test.csv"
    final_out = using_visual_data(time_speaker, path)
    print(final_out)
