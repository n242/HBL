import os
from moviepy.editor import VideoFileClip

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
    if(percent_speaker0>percent_speaker1):
        for i in range(len(diarization)):
            if(diarization[i][2] == "SPEAKER_00"):
                diarization[i][2] = "S"
            elif(diarization[i][2] == "SPEAKER_01"):
                diarization[i][2] = "I"
    else:
        for i in range(len(diarization)):
            if(diarization[i][2] == "SPEAKER_00"):
                diarization[i][2] = "I"
            elif(diarization[i][2] == "SPEAKER_01"):
                diarization[i][2] = "S"
    return diarization

def convert_mp4_to_wav(mp4_path, wav_path):
    video_clip = VideoFileClip(mp4_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(wav_path)