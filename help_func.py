import os
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm
import visualization
from main import Diarization
import soundfile as sf
from scipy.io import wavfile

def get_file_format(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.mp4':
        return 'MP4'
    elif file_extension == '.wav':
        return 'WAV'
    else:
        return 'Unknown'

def diarization_get_spaker(dir):
    diarization = [list(item) for item in dir]
    sum = 0
    sum0 = 0
    sum1 = 1
    for i in range(len(diarization)):
        sum += (diarization[i][1] - diarization[i][0])
        if(diarization[i][2] == "SPEAKER_00"):
            sum0 += (diarization[i][1] - diarization[i][0])
        elif(diarization[i][2] == "SPEAKER_01"):
            sum1 += (diarization[i][1] - diarization[i][0])
    percent_speaker0 = sum0/sum
    percent_speaker1 = sum1/sum
    if (diarization[0][2] == "SPEAKER_00"):
        if(percent_speaker0 > percent_speaker1):
            print("MAYBE INVALID SPEAKER CONVERSION!! marissa percent: ", percent_speaker0)
        for i in range(len(diarization)):
            if(diarization[i][2] == "SPEAKER_00"):
                diarization[i][2] = "I"
            elif(diarization[i][2] == "SPEAKER_01"):
                diarization[i][2] = "S"
    else:
        if(percent_speaker1 > percent_speaker0):
            print("MAYBE INVALID SPEAKER CONVERSION!! marissa percent: ", percent_speaker1)
        for i in range(len(diarization)):
            if(diarization[i][2] == "SPEAKER_00"):
                diarization[i][2] = "S"
            elif(diarization[i][2] == "SPEAKER_01"):
                diarization[i][2] = "I"
    return diarization

def convert_mp4_to_wav(mp4_path, wav_path):
    video_clip = VideoFileClip(mp4_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_path)

def create_data_for_1TO10():
    print("Creating data for all") #use tqdm to see progress
    parent_path = "/media/faisal/RE_AS/REASEARCHASSISTANT/RECORDS/"
    list_paths = ["record1/1_EMOTIONS_BOTH.mp4",
                  "record1/1_STORY_BOTH.mp4",
                  "record1/1_TB_BOTH.mp4",
                  "record2/2_EMOTIONS_BOTH.mp4",
                  "record2/2_STORY_BOTH.mp4",
                  "record2/2_TB_BOTH.mp4",
                  "record3/3_EMOTIONS_BOTH.mp4",
                  "record3/3_STORY_BOTH.mp4",
                  "record3/3_TB_BOTH.mp4",
                  "record4/4_EMOTIONS_BOTH.mp4",
                  "record4/4_STORY_BOTH.mp4",
                  "record4/4_TB_BOTH.mp4",
                  "record5/5_EMOTIONS_MARISSA.mp4",
                  "record5/5_STORY_SUBJECT.mp4",
                  "record5/5_TB_SUBJECT.mp4",
                  "record6/6_EMOTIONS_BOTH.mp4",
                  "record6/6_STORY_BOTH.mp4",
                  "record6/6_TB_BOTH.mp4",
                  "record7/7_EMOTIONS_BOTH.mp4",
                  "record7/7_TB_BOTH.mp4",
                  "record8/8_EMOTIONS_BOTH.mp4",
                  "record8/8_STORY_BOTH.mp4",
                  "record8/8_TB_BOTH.mp4",
                  "record9/9_EMOTIONS_BOTH.mp4",
                  "record9/9_STORY_BOTH.mp4",
                  "record9/9_TB_BOTH.mp4",
                  "record10/10_EMOTIONS_BOTH.mp4",
                  "record10/10_STORY_BOTH.mp4",
                  "record10/10_TB_BOTH.mp4",
                  "record9/9_EMOTIONS_SUBJECT.mp4"
                  "record8/8_STORY_MARISSA.mp4"
                  "record1/1_STORY_MARISSA.mp4"
                  ]
    for i in tqdm(list_paths, desc="Processing"):
        path = parent_path + i
        file_name = os.path.splitext(os.path.basename(path))[0]
        print("Doing for: " + path)
        new_file_path = os.path.splitext(path)[0] + "." + "wav"
        convert_mp4_to_wav(path, new_file_path)
        path = new_file_path
        flag = True
        data, sampling_rate = sf.read(path)
        samplerate, data_arr = wavfile.read(path)
        channel = data_arr[:, 0]  # Extract left channel
        visual = visualization.Vizualization(path, sampling_rate, data, channel)
        diarization = Diarization(path)
        diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
        if flag:
            os.remove(path)
        new_diarization = diarization_get_spaker(diarization_smooth)
        diarization.pyannote_diarization_csv(new_diarization, path='RESULTS1_10/'+file_name)

def create_data_for_11TO21():
    print("Creating data for all") #use tqdm to see progress
    parent_path = "/media/faisal/RE_AS/REASEARCHASSISTANT/RECORDS/"
    list_paths = [#"record11/Emotions/Subject_1.mp4",
                #   "record11/story/Both_1.mp4",
                #   "record11/TB/Both_1.mp4",
                #   "record12/Emotions/Both_1.mp4",
                #   "record12/story/Both_1.mp4",
                #   "record12/TB/Both_1.mp4",
                #   "record13/Emotions/Subject_1.mp4",
                #   "record13/story/Both_1.mp4",
                #   "record13/TB/Both_1.mp4",
                #   "record14/Emotions/SUBJwavfileECT2_1.mp4",
                #   "record14/story/BOTH2_1.mp4",
                #   "record14/TB/BOTH2_1.mp4",
                #   "record15/Emotions/SUBJECT2_1.mp4",
                #   "record15/story/BOTH1_1.mp4",
                #   "record15/TB/BOTH2_1.mp4",
                #   "record16/Emotions/Both_1.mp4",
                #   "record16/story/Both_1.mp4",
                #   "record16/TB/Both_1.mp4",
                #   "record17/Emotions/Subject_1.mp4",
                #   "record17/story/Both_1.mp4",
                #   "record17/TB/Both_1.mp4",
                #   "record18/Emotions/BOTH_1.mp4",
                #   "record18/story/BOTH_1.mp4",
                #   "record18/TB/BOTH_1.mp4",
                #   "record19/Emotions/Both_1.mp4",
                #   "record19/story/Both_1.mp4",
                #   "record19/TB/Both_1.mp4",
                #   "record20/Emotions/20_EMOTIONS_SUBJECT.mp4",
                #   "record20/story/Both_1.mp4",
                #   "record20/TB/Both_1.mp4",
                #   "record21/Emotions/Both_1.mp4",
                #   "record21/story/Both_1.mp4",
                #   "record21/TB/Both_1.mp4",
                #   "record22/Emotions/Both_1.mp4",
                #   "record22/story/Both_1.mp4",
                #   "record22/TB/Both_1.mp4",
                #   "record23/Emotions/Both_1.mp4",
                #   "record23/story/Both_1.mp4",
                #   "record23/TB/Both_1.mp4",
                #   "record24/Emotions/Both_1.mp4",
                #   "record24/story/Marissa_1.mp4",
                #   "record24/TB/Both_1.mp4",
                #   "record25/Emotions/Both_1.mp4",
                #   "record25/story/Both_1.mp4",
                #   "record25/TB/Marissa_1.mp4",
                #   "record26/Emotions/BOTH2_1.mp4",
                #   "record26/story/Marissa2_1.mp4",
                #   "record26/TB/BOTH2_1.mp4",
                #   "record27/Emotions/Both_1.mp4",
                #   "record27/story/Both_1.mp4",
                #   "record27/TB/Marissa_1.mp4",
                #   "record28/Emotions/Both_1.mp4",
                #   "record28/story/Marissa_1.mp4",
                #   "record28/TB/Both_1.mp4",
                #   "record29/Emotions/Both_1.mp4",
                #   "record29/story/Marissa_1.mp4",
                #   "record29/TB/Both_1.mp4",
                #   "record30/Emotions/Both_1.mp4",
                #   "record30/story/Marissa_1.mp4",
                #   "record30/TB/Marissa_1.mp4",
                #   "record31/Emotions/Both_1.mp4",
                #   "record31/story/Both_1.mp4",
                #   "record31/TB/Both_1.mp4",
                #   "record32/Emotions/Both_1.mp4",
                #   "record32/story/Both_1.mp4",
                #   "record32/TB/Both_1.mp4",
                #   "record33/Emotions/Marissa_1.mp4",
                #   "record33/story/Marissa_1.mp4",
                #   "record33/TB/Both_1.mp4",
                #   "record34/Emotions/Marissa_1.mp4",
                #   "record34/story/Both_1.mp4",
                #   "record34/TB/Both_1.mp4",
                #   "record35/Emotions/Both_1.mp4",
                #   "record35/story/Both_1.mp4",
                #   "record35/TB/Both_1.mp4",
                #   "record36/Emotions/Marissa_1.mp4",
                #   "record36/story/Both_1.mp4",
                #   "record36/TB/Both_1.mp4",
                #   "record37/Emotions/Both_1.mp4",
                #   "record37/story/Both_1.mp4",
                #   "record37/TB/Both_1.mp4",
                #   "record38/Emotions/Both_1.mp4",
                #   "record38/story/Both_1.mp4",
                #   "record38/TB/Both_1.mp4",
                #   "record39/Emotions/Both_1.mp4",
                #   "record39/Book/Both_1.mp4",
                #   "record39/TB/Both_1.mp4",
                #   "record40/Emotions/Both_1.mp4",
                #   "record40/Story/Marissa_1.mp4",
                #   "record40/TB/Both_1.mp4",
                  ]
    for i in tqdm(list_paths, desc="Processing"):
        path = parent_path + i
        record_index = i.index("record") + len("record")
        number = int(i[record_index:record_index+2])
        directories = i.split("/")
        second_parent_directory = directories[1]
        file_name = os.path.splitext(os.path.basename(path))[0]
        name_before_underscore = file_name.split("_")[0]
        file_name = str(number) + "_" + second_parent_directory + "_" + name_before_underscore
        print(file_name)
        print("Doing for: " + path)
        new_file_path = os.path.splitext(path)[0] + "." + "wav"
        convert_mp4_to_wav(path, new_file_path)
        path = new_file_path
        flag = True
        data, sampling_rate = sf.read(path)
        samplerate, data_arr = wavfile.read(path)
        channel = data_arr[:, 0]  # Extract left channel
        visual = visualization.Vizualization(path, sampling_rate, data, channel)
        diarization = Diarization(path)
        diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
        if flag:
            os.remove(path)
        new_diarization = diarization_get_spaker(diarization_smooth)
        diarization.pyannote_diarization_csv(new_diarization, path='RESULTS11_21/'+file_name)

def create_data_for_rest220():
    print("Creating data for all") #use tqdm to see progress
    parent_path = "/media/faisal/RE_AS/REASEARCHASSISTANT/RECORDS/"
    list_paths = [#"record142/142_EMO_I.mp4",
                #   "record142/142_Story_I.mp4",
                #   "record142/142_TB_I.mp4",
                #   "record144/144_EMO_I.mp4",
                #   "record144/144_TB_I.mp4",
                #   "record203/203_EMO_B.mp4",
                #   "record203/203_Story_B.mp4",
                #   "record203/203_TB_B.mp4",
                #   "record204/204_EMO_B.mp4",
                #   "record204/204_Story_B.mp4",
                #   "record204/204_TB_B.mp4",
                #   "record205/205_EMO_B.mp4",
                #   "record205/205_Story_B.mp4",
                #   "record205/205_TB_B.mp4",
                #   "record209/209_EMO_B.mp4",
                #   "record209/209_Story1_B.mp4",
                #   "record209/209_Story2_B.mp4",
                #   "record209/209_TB_B.mp4",
                #   "record213/213_EMO_B.mp4",
                #   "record213/213_Story1_B.mp4",
                #   "record213/213_Story2_B.mp4",
                #   "record213/213_TB_B.mp4",
                #   "record214/214_EMO_B.mp4",
                #   "record214/214_Story_B.mp4",
                #   "record214/214_TB_B.mp4",
                #   "record215/215_EMO_B.mp4",
                #   "record215/215_Story_B.mp4",
                #   "record215/215_TB_B.mp4",
                #   "record218/218_EMO_B.mp4",
                #   "record218/218_Story_B.mp4",
                #   "record218/218_TB_B.mp4",
                #   "record220/220_EMO_B.mp4",
                #   "record220/220_Story_B.mp4",
                #   "record220/220_TB_B.mp4",
                  ]
    for i in tqdm(list_paths, desc="Processing"):
        path = parent_path + i
        file_name = os.path.splitext(os.path.basename(path))[0]
        print("Doing for: " + path)
        new_file_path = os.path.splitext(path)[0] + "." + "wav"
        convert_mp4_to_wav(path, new_file_path)
        path = new_file_path
        flag = True
        data, sampling_rate = sf.read(path)
        samplerate, data_arr = wavfile.read(path)
        channel = data_arr[:, 0]  # Extract left channel
        visual = visualization.Vizualization(path, sampling_rate, data, channel)
        diarization = Diarization(path)
        diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
        if flag:
            os.remove(path)
        new_diarization = diarization_get_spaker(diarization_smooth)
        diarization.pyannote_diarization_csv(new_diarization, path='RESULTS_REST/'+file_name)

def create_data_for_rest():
    print("Creating data for all") #use tqdm to see progress
    parent_path = "/media/faisal/RE_AS/REASEARCHASSISTANT/RECORDS/"
    list_paths = [#"record222/Done222/emotions_marissa.mp4",
                #   "record222/Done222/story_subject.mp4",
                #   "record222/Done222/TB_marissa.mp4",
                #   "record223/Done223/emotions_subject.mp4",
                #   "record223/Done223/story_marissa.mp4",
                #   "record223/Done223/TB_both.mp4",
                #   "record224/Done224/emotions_marissa.mp4",
                #   "record224/Done224/story_both.mp4",
                #   "record224/Done224/TB_marissa.mp4",
                #   "record225/Done225/emosions_subject.mp4",
                #   "record225/Done225/story_marissa.mp4",
                #   "record225/Done225/TB_marissa.mp4",
                #   "record226/Done226/emotions_both.mp4",
                #   "record226/Done226/story_marissa.mp4",
                #   "record226/Done226/TB_marissa.mp4",
                #   "record227/done227/emotions_marissa.mp4",
                #   "record227/done227/story_subject.mp4",
                #   "record227/done227/TB_marissa.mp4",
                  #________________________________________________________________________
                #   "record228/Done228/228_Emotions_both.mp4",
                #   "record228/Done228/228_Story_both.mp4",
                #   "record228/Done228/228_TB_both.mp4",
                #   "record229/Done229/229_Emotions_subject.mp4",
                #   "record229/Done229/229_story_both.mp4",
                #   "record229/Done229/229_TB_both.mp4",
                #   "record230/Done230/230_emotions_both.mp4",
                #   "record230/Done230/230_story_both.mp4",
                #   "record230/Done230/230_TB_both.mp4",
                #   "record231/Done231/231_emotions_both.mp4",
                #   "record231/Done231/231_story_both.mp4",
                #   "record231/Done231/231_TB_both.mp4",
                #   "record232/Done232/232_emotions_both.mp4",
                #   "record232/Done232/232_story_both.mp4",
                #   "record232/Done232/232_TB_both.mp4",
                #   "record233/Done233/233_emotions_subject.mp4",
                #   "record233/Done233/233_story_both.mp4",
                #   "record233/Done233/233_TB_both.mp4",
                #   "record234/Done234/234_Emotions_both.mp4",
                #   "record234/Done234/234_Story_both.mp4",
                #   "record234/Done234/234_TB_both.mp4",
                #   "record235/Done235/235_Emotions_both.mp4",
                #   "record235/Done235/235_Story_both.mp4",
                #   "record235/Done235/235_TB_both.mp4",
                  ]
    for i in tqdm(list_paths, desc="Processing"):
        path = parent_path + i
        file_name = os.path.splitext(os.path.basename(path))[0]
        print("File name: ", file_name)
        print("Doing for: " + path)
        new_file_path = os.path.splitext(path)[0] + "." + "wav"
        convert_mp4_to_wav(path, new_file_path)
        path = new_file_path
        flag = True
        data, sampling_rate = sf.read(path)
        samplerate, data_arr = wavfile.read(path)
        channel = data_arr[:, 0]  # Extract left channel
        visual = visualization.Vizualization(path, sampling_rate, data, channel)
        diarization = Diarization(path)
        diarization_smooth, raw_diarization = diarization.legal_diarization_smoothing()
        if flag:
            os.remove(path)
        new_diarization = diarization_get_spaker(diarization_smooth)
        diarization.pyannote_diarization_csv(new_diarization, path='RESULTS_REST2/'+file_name)

def add_audio_to_mp4(mp4_path, audio_path, output_path):
    # Load the video clip
    video = VideoFileClip(mp4_path)

    # Load the audio clip
    audio = AudioFileClip(audio_path)

    # Set the audio of the video clip
    video = video.set_audio(audio)

    # Write the final video with the added audio to the output path
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")