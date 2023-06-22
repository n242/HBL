# importing vlc module
import os
os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
import vlc
import tkinter
import time
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard
import openpyxl
from Files import *
import os.path
from Excel import *
from datetime import datetime


class customMP:
    # creating vlc media player object
    def __init__(self):
            self.video_file = get_file("Please select the video file")
            self.media_player = vlc.MediaPlayer(self.video_file)
            self.times = []  # List to store time segments with 'I' or 'S'
            self.I_is_speaking = False
            self.I_current_start_time = 0
            self.S_is_speaking = False
            self.S_current_start_time = 0 
            self.pause_flag = 0
            self.fr = (1/25)
    
    def on_press(self, key):
        try:
            if (key.char == 'a' or key.char == 'A' or key.char == 'ש') and not self.I_is_speaking:
                self.I_current_start_time = self.media_player.get_time()
                print(self.I_current_start_time)
                self.I_is_speaking = True
            if (key.char == 'd' or key.char == 'D' or key.char == 'ג') and not self.S_is_speaking:
                self.S_current_start_time = self.media_player.get_time()
                print(self.S_current_start_time)
                self.S_is_speaking = True
        except AttributeError:
            print('special key pressed: {0}'.format(key))

    def on_release(self, key):
        if key == keyboard.Key.space:
            self.media_player.pause()
        if key == keyboard.Key.right:
            cur_time = self.media_player.get_time()
            print("cur time", cur_time)
            self.media_player.set_time(cur_time + int(self.fr * 1000))
        if key == keyboard.Key.left:
            cur_time = self.media_player.get_time()
            print("cur time", cur_time)
            self.media_player.set_time(cur_time - int(self.fr * 1000))
        if key == keyboard.Key.esc:
            return False
        try:
            if key.char == 'a' or key.char == 'ש':
                self.times.append(("I", self.I_current_start_time, self.media_player.get_time()))
                self.I_is_speaking = False
                print("end")
            if key.char == 'd' or key.char == 'ג':
                cur_time = self.media_player.get_time()
                self.times.append(("S", self.S_current_start_time, cur_time))
                self.S_is_speaking = False
                print("end : ", cur_time)
            if key.char == 't' or key.char == 'א':
                print('time is: ', self.media_player.get_time())
            if key.char == '[':
                print('play rate :', self.media_player.get_rate() - 0.1)
                self.media_player.set_rate(self.media_player.get_rate() - 0.1)
            if key.char == ']':
                print('play rate :', self.media_player.get_rate() + 0.1)
                self.media_player.set_rate(self.media_player.get_rate() + 0.1)
            if key.char == 'r' or key.char == 'ר':
                print("list reset")
                self.times = []
            if key.char == 'l':
                self.media_player.pause()
                self.media_player.set_time(0)
            if key.char == 'z' or key.char == 'ז':
                print("last delete")
                if len(self.times) > 0:
                    del self.times[-1]
        except AttributeError:
            print('special key pressed: {0}'.format(key))
    
    def play_video(self):
        self.media_player.set_rate(1)
        self.media_player.play()
        ptime = 0
        self.media_player.set_time(ptime)
        time.sleep(1)
        self.media_player.pause()
        self.media_player.set_time(ptime)
        self.media_player.pause()
        self.fr = 1 / self.media_player.get_fps()
        print('fr ', self.fr)
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
    
    def get_video_file(self):
        return self.video_file


# Collect events until released
# https://stackoverflow.com/questions/47990695/how-to-embed-a-vlc-instance-in-a-tkinter-frame
mp = customMP()
mp.play_video()

name = os.path.basename(mp.video_file)
base = name.split(".")[0]

base = base + " " + now_file_format()
xl_file = os.path.dirname(mp.video_file) + "\\" + base

if mp.times:
    print(*mp.times, sep='\n')
    append_write(xl_file + ".xlsx", mp.times)
else:
    print("nothing to save")

# printing type of media player variable
