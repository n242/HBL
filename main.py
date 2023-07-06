from pyannote.audio import Pipeline
from scipy.io.wavfile import read as read_wav
import pandas as pd
from moviepy.editor import VideoFileClip
import visualization
import soundfile as sf
import noise_clean


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

def diarization_w_smoothing(my_wav):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")
    diarization = pipeline(my_wav)
    times = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        #print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        if len(times) >= 1 and times[-1][2] == speaker and abs(turn.start - times[-1][1]) < 1:
            # print(f"concatenated at{turn.end}")
            times[-1] = ((times[-1][0], round(turn.end, 1), speaker))
        else:
            times.append((round(turn.start, 1), round(turn.end, 1), speaker))
    for i in range(len(times)):
        print(times[i])
    return times, diarization

def legal_diarization_smoothing(my_wav):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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")
    diarization = pipeline(my_wav)
    times = []
    #TODO: add dictionary of speakers count how many times it detects each speaker
    speakers={"SPEAKER_00":0, "SPEAKER_01":0}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if str(speaker)=="SPEAKER_02":
            print("detected 3 speakers, bad diarization")
        #print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        if len(times) >= 1 and times[-1][2] == speaker and abs(turn.start - times[-1][1]) < 1:
            # print(f"concatenated at{turn.end}")
            times[-1] = ((times[-1][0], round(turn.end, 1), speaker))
            speakers[speaker] += 1
        else:
            times.append((round(turn.start, 1), round(turn.end, 1), speaker))
            speakers[speaker]+=1
    if len(times)>3:   # check diarization is only for one speaker for the longer vids
        for key, val in speakers.items():
            if val<3:
                print(f"speaker {key} had only {val} occurences")
    for i in range(len(times)):
        print(times[i])
    return times, diarization


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


def main_excel():
    csv2 = 'data/220_EMO_I.csv'
    wav2 = "data/220_EMO_I.wav"
    out2 = run_s_i(csv2, wav2)

    csv1 = 'data/220_EMO_S.csv'
    wav1 = "data/220_EMO_S.wav"
    out1 = run_s_i(csv1, wav1)

    compare_outputs(out1, out2)


def convert_mp4_to_wav(mp4_path, wav_path):
    video_clip = VideoFileClip(mp4_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_path)

if __name__ == '__main__':

    # mp4_file = 'E:/myFolder/uni/masters/2nd_semestru/human_behavior_lab/noise_clean_recordings/1_TB_SUBJECT.mp4 '
    # wav_file = 'E:/myFolder/uni/masters/2nd_semestru/human_behavior_lab/noise_clean_recordings/1_TB_SUBJECT.wav'
    # convert_mp4_to_wav(mp4_file, wav_file)
    wav1 = "data/1_STORY_SUBJECT.wav"
    print("diarizing: " + wav1)

    diarization_smooth, diarization = diarization_w_smoothing(wav1)
    
    # sampling_rate, data = read_wav(wav1)
    data, sampling_rate = sf.read(wav1)
    visual = visualization.Vizualization(wav1, sampling_rate, data)

    list_speaker_times0 = visual.diarization_for_plot(diarization_smooth)
    # visual.plot_animation(list_speaker_times0)
    # visual.plot_diarization(list_speaker_times0)

    list_speaker_times1 = visual.diarization_for_plot1(diarization_smooth)
    visual.plot_animation2(list_speaker_times1) #Animation with background audio, works with diarization_for_plot1

    time_speaker = legal_diarization_smoothing(wav1)


