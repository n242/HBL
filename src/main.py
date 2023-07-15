from pyannote.audio import Pipeline
import pandas as pd
import soundfile as sf
import os

import help_func
import noise_clean
import visualization

class Diarization:
    def __init__(self, wav, auth_token):
        self.wav = wav
        self.auth_token = auth_token

    #basic diarization
    def pyannote_diarization(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token=self.auth_token)

        # apply pretrained pipeline
        diarization = pipeline(self.wav)

        # print the result and save to arr
        times = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
            times.append((round(turn.start, 1), round(turn.end, 1), speaker))
        return times

    # diarization with hysteresis
    def diarization_w_smoothing(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                            use_auth_token=self.auth_token)
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
                                            use_auth_token=self.auth_token)
        diarization = pipeline(self.wav)
        times = []
        speakers = {"SPEAKER_00": 0, "SPEAKER_01": 0, "SPEAKER_02": 0}
        error_msg = ""
        for turn, _, speaker in diarization.itertracks(yield_label=True):
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
        elif len(times) > 10:  # check diarization is only for one speaker for the longer vids
            for key, val in speakers.items():
                if val <= 4:
                    error_msg=f"BAD DIARIZATION: speaker {key} had only {val} occurences"
        print(error_msg)
        for i in range(len(times)):
            print(times[i])
        return times, diarization, error_msg

    #generating .csv from diarization
    def pyannote_diarization_csv(self, times, path):
        start_times = list(zip(*times))[0]
        stop_times = list(zip(*times))[1]
        speakers = list(zip(*times))[2]

        if speakers[0]=="SPEAKER_00":
            new_speakers = ["I" if speaker=="SPEAKER_00" else "S" for speaker in speakers]
        else:
            new_speakers = ["S" if speaker == "SPEAKER_00" else "I" for speaker in speakers]

        # Create a DataFrame from the arrays
        data = {'start': start_times, 'stop': stop_times, 'speaker': new_speakers}
        df = pd.DataFrame(data)

        # Save the DataFrame to Excel
        filename = path + '.csv'
        df.to_csv(filename, index=False)

        print(f"CSV file '{filename}' created successfully.")


# create diarization and output to .csv
def main_diarizaion(wav1, auth_token):
    file_name = os.path.splitext(os.path.basename(wav1))[0]
    print("diarizing: " + wav1)
    # if file is .mp4 format, then transform to .wav format
    flag = False
    if (help_func.get_file_format(wav1) == 'MP4'):
        new_file_path = os.path.splitext(wav1)[0] + "." + "wav"
        help_func.convert_mp4_to_wav(wav1, new_file_path)
        wav1 = new_file_path
        flag = True
    elif (help_func.get_file_format(wav1) == 'Unknown'):
        raise Exception("ERROR WRONG FILE TYPE")

    # apply diarization
    diarization = Diarization(wav1, auth_token)
    diarization_smooth, raw_diarization, error_msg = diarization.legal_diarization_smoothing()

    #generating .csv file of the diarization output
    current_directory = os.getcwd()
    # Specify the path to the "results" folder relative to the current directory
    results_folder = os.path.join(current_directory, '..', 'results/')

    diarization.pyannote_diarization_csv(diarization_smooth, path=results_folder + file_name)

    # #check if we got bad diarization, if so apply noise cleaning and try again
    if error_msg != "":
        noise_clean.clean_audio(wav1)
        print("diarization after noise cleaning")
        wav2 = wav1[:-4] + "_edited.wav"
        diarization = Diarization(wav2, auth_token)
        diarization_smooth, raw_diarization, error_msg = diarization.legal_diarization_smoothing()
        diarization.pyannote_diarization_csv(diarization_smooth, path=results_folder + file_name)

    if flag:
        os.remove(wav1)
    return diarization_smooth, file_name

# main function to generate .png plot file, .mp4 animation of the diarization
def main_visualization(wav1, diarization_smooth, file_name):
    data, sampling_rate = sf.read(wav1)
    visual = visualization.Vizualization(wav1, sampling_rate, data)
    list_speaker_times = visual.diarization_for_plot1(diarization_smooth)
    current_directory = os.getcwd()
    # Specify the paths to the visuals folders relative to the current directory
    visuals_folder = os.path.join(current_directory, '..', 'visual_outputs/')
    out_audios_folder = os.path.join(current_directory, '..', 'output_wavs/')

    #generating image plot
    visual.plot_diarization(list_speaker_times, path=visuals_folder + file_name)

    # generating animation gif from diarization
    visual.plot_animation2(list_speaker_times, path=visuals_folder +  file_name)

    # combining .gif with .wav to create .mp4 diarization for vid
    visual.create_vid_from_gif(visuals_folder + file_name + 'animation2.gif', out_audios_folder ,visuals_folder + file_name + ".mp4")


if __name__ == '__main__':
    print("diarization before noise cleaning")
    # input can be .mp4 or .wav file
    current_directory = os.getcwd()
    # Specify the paths to the visuals folders relative to the current directory
    data = os.path.join(current_directory, '..', 'data/')

    wav1 =data+ "YOUR INPUT PATH" ".wav"

    # replace the auth token with your input
    auth_token = "YOUR INPUT AUTH"
    # diarize
    diarization_smooth, file_name = main_diarizaion(wav1, auth_token)


    #if wanting to see visual results run:
    main_visualization(wav1, diarization_smooth, file_name)


