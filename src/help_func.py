import os
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm
import soundfile as sf
from scipy.io import wavfile
import tkinter as tk
from tkinter import filedialog
import visualization
from main import Diarization

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

def add_audio_to_mp4(mp4_path, audio_path, output_path):
    # Load the video clip
    video = VideoFileClip(mp4_path)

    # Load the audio clip
    audio = AudioFileClip(audio_path)

    # Set the audio of the video clip
    video = video.set_audio(audio)

    # Write the final video with the added audio to the output path
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP4 files", "*.mp4")])
    return file_path