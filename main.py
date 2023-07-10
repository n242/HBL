from pyannote.audio import Pipeline
import pandas as pd
import soundfile as sf
import os
from help_func import *
from tqdm import tqdm


from help_func import *
import noise_clean
import visualization

class Diarization:
    def __init__(self, wav):
        self.wav = wav

    #basic diarization
    def pyannote_diarization(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token="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")

        # 4. apply pretrained pipeline
        diarization = pipeline(self.wav)

        # 5. print the result and save to arr
        times = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            times.append((round(turn.start, 1), round(turn.end, 1), speaker))
        return times

    def diarization_w_smoothing(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token="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")
        diarization = pipeline(self.wav)
        times = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            if len(times) >= 1 and times[-1][2] == speaker and abs(turn.start - times[-1][1]) < 1:
                # print(f"concatenated at{turn.end}")
                times[-1] = ((times[-1][0], round(turn.end, 1), speaker))
            else:
                times.append((round(turn.start, 1), round(turn.end, 1), speaker))
        for i in range(len(times)):
            print(times[i])
        return times, diarization

    # diarization with hysteresis + check it's valid diarization
    def legal_diarization_smoothing(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token="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")
        diarization = pipeline(self.wav)
        times = []
        speakers = {"SPEAKER_00": 0, "SPEAKER_01": 0, "SPEAKER_02": 0}
        error_msg = ""
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            if len(times) >= 1 and times[-1][2] == speaker and abs(turn.start - times[-1][1]) < 1:
                # applied smoothing, connecting to prev segment
                times[-1] = ((times[-1][0], round(turn.end, 1), speaker))
                speakers[speaker] += 1
            else:
                times.append((round(turn.start, 1), round(turn.end, 1), speaker))
                speakers[speaker] += 1
        # validity tests of diarization below
        if speakers["SPEAKER_02"]!=0:
            error_msg="BAD DIARIZATION: detected 3 speakers"
        speakers.pop("SPEAKER_02")
        if speakers["SPEAKER_01"]==0:
            error_msg="BAD DIARIZATION: only 1 speaker detected"
        elif len(times) > 3:  # check diarization is only for one speaker for the longer vids
            for key, val in speakers.items():
                if val <= 3:
                    error_msg=f"BAD DIARIZATION: speaker {key} had only {val} occurences"
        print(error_msg)
        for i in range(len(times)):
            print(times[i])
        return times, diarization

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

    def run_s_i(self, csv1, wav):
        self.wav = wav
        time_speaker = self.pyannote_diarization()
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

    def pyannote_diarization_csv(self, times, path):
        start_times = list(zip(*times))[0]
        stop_times = list(zip(*times))[1]
        speakers = list(zip(*times))[2]

        # Create a DataFrame from the arrays
        data = {'start': start_times, 'stop': stop_times, 'speaker': speakers}
        df = pd.DataFrame(data)

        # Save the DataFrame to Excel
        filename = path + '.csv'
        df.to_csv(filename, index=False)

        print(f"CSV file '{filename}' created successfully.")

    def pyannote_diarization_xlsx(self, times, path):
        start_times = list(zip(*times))[0]
        stop_times = list(zip(*times))[1]
        speakers = list(zip(*times))[2]


def faisal_diarization():
    # create_data_for_rest()
    path = "/home/faisal/Desktop/interview_example1.wav"
    file_name = os.path.splitext(os.path.basename(path))[0]
    flag = False
    if(get_file_format(path) == 'MP4'):
        new_file_path = os.path.splitext(path)[0] + "." + "wav"
        convert_mp4_to_wav(path, new_file_path)
        path = new_file_path
        flag = True
    elif(get_file_format(path) == 'Unknown'):
        raise Exception("ERROR WRONG FILE TYPE")
    
    print("diarizing: " + path)

    data, sampling_rate = sf.read(path)
    visual = visualization.Vizualization(wav1, sampling_rate, data)

    diarization = Diarization(path)
    diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
    if flag:
        os.remove(path)
    new_diarization = diarization_get_spaker(diarization_smooth)
    diarization.pyannote_diarization_csv(new_diarization, path='/home/faisal/Desktop/'+file_name)
    list_speaker_times = visual.diarization_for_plot1(new_diarization)
    visual.plot_diarization(list_speaker_times, path='/home/faisal/Desktop/' + file_name)
    visual.plot_animation2(list_speaker_times, '/home/faisal/Desktop/' + file_name, path)  # Animation with background audio, works with diarization_for_plot1



def main_diarizaion(wav1):
    file_name = os.path.splitext(os.path.basename(wav1))[0]
    print("diarizing: " + wav1)
    flag = False
    if (get_file_format(wav1) == 'MP4'):
        new_file_path = os.path.splitext(wav1)[0] + "." + "wav"
        convert_mp4_to_wav(wav1, new_file_path)
        wav1 = new_file_path
        flag = True
    elif (get_file_format(wav1) == 'Unknown'):
        raise Exception("ERROR WRONG FILE TYPE")

    diarization = Diarization(wav1)
    diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
    diarization.pyannote_diarization_csv(diarization_smooth, path='results/' + file_name)
    if flag:
        os.remove(path)
    return diarization_smooth, file_name


def main_visualization(wav1, diarization_smooth, file_name):

    data, sampling_rate = sf.read(wav1)
    visual = visualization.Vizualization(wav1, sampling_rate, data)
    list_speaker_times = visual.diarization_for_plot1(diarization_smooth)
    visual.plot_diarization(list_speaker_times, path='visual_outputs/' + file_name)
    visual.plot_animation2(list_speaker_times,
                           path='visual_outputs/' + file_name)  # Animation with background audio, works with diarization_for_plot1

    visual.create_vid_from_gif('visual_outputs/' + file_name + 'animation2.gif', "visual_outputs/" + file_name + ".mp4")

if __name__ == '__main__':
    path = "data/to_classify/40_Story_Marissa_1.wav"
    noise_clean.clean_audio(path)

    wav1 ="data/to_classify/40_Story_Marissa_1_edited.wav"
    diarization_smooth, file_name = main_diarizaion(wav1)

    #if wanting to see visual results run:
    #main_visualization(wav1, diarization_smooth, file_name)

