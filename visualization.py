from sys import stderr
from time import sleep, perf_counter as timer
from typing import Iterable, TypeVar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import sounddevice as sd
import matplotlib.lines as mlines
from matplotlib import colors as mlpColors
<<<<<<< HEAD
import matplotlib
from help_func import *
matplotlib.use('agg')
=======
>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93

_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


class Vizualization:
    def __init__(self, wav, sampling_rate, data, data_arr):
        self.SAMPLE_RATE = sampling_rate
        self.wav = wav
        self.audio = data
        self.times_list = []
        self.data_arr = data_arr

    def play_wav(self, blocking=True):
        try:
            # Small bug with sounddevice.play: the audio is cut 0.5 second too early. so we pad it
            # Convert self.wav to a NumPy array

            data = self.data_arr.astype(np.int16)

            # Concatenate zeros to the waveform
            zeros = np.zeros(self.SAMPLE_RATE // 2, dtype=np.int16)
            data = np.concatenate((data, zeros))

            # Play the audio using sd.play()
            sd.play(data, self.SAMPLE_RATE, blocking=blocking)

        except Exception as e:
            print("Failed to play audio: %s" % repr(e))

    def diarization_for_plot1(self, gen_diarization):
        final_list = []
        max_diar = len(gen_diarization)
        times = np.arange(0, gen_diarization[-1][1], 1)  # arr from 0 to end of audio
        # print(times.shape)
        j = 0
        for i in range(len(times)):
            if j < max_diar:
                if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
                    if gen_diarization[j][2] == "I":
                        final_list.append(1)
                    else:
                        final_list.append(2)

                elif times[i] > gen_diarization[j][1]:  # no speaker
                    final_list.append(0)
                    j += 1
                else:
                    final_list.append(0)
        return final_list

    def plot_diarization(self, final_list, path):

        times = np.arange(0, len(final_list), 1)  # arr from 0 to end of audio

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.suptitle('Speaker Diarization')
<<<<<<< HEAD
        colors = ['black', 'red', 'blue']
        T = TypeVar('T', int, float)  # Create a generic type variable
        levels: Iterable[T] = [0, 1, 2]  # Use the generic type variable T
=======

        color_dict = {
            0: ('black', 'No Speaker'),
            1: ('red', 'Interviewee'),
            2: ('blue', 'Marissa')
        }

        colors = [color_dict[val][0] for val in final_list]
        labels = [color_dict[val][1] for val in final_list]

>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93
        black_line = mlines.Line2D([], [], color='black', marker='.', markersize=15, label='No Speaker')
        red_line = mlines.Line2D([], [], color='red', marker='.', markersize=15, label='Interviewee')
        blue_line = mlines.Line2D([], [], color='blue', marker='.', markersize=15, label='Interviewer')

        ax.legend(fontsize='small', title='Speakers:', handles=[black_line, red_line, blue_line])

<<<<<<< HEAD
        cmap, norm = mlpColors.from_levels_and_colors(levels=levels, colors=colors, extend='max')
        timeDiffInt = np.where(np.array(final_list) == 0, 0, np.where(np.array(final_list) == 1, 2, 1))
        ax.scatter(times, final_list, c=timeDiffInt, s=150, marker='.', edgecolor='none', cmap=cmap, norm=norm,
                label=("No Speaker", "Marissa", "Interviewee"))
=======
        T = TypeVar('T', int, float)  # Create a generic type variable
        levels: Iterable[T] = [0, 1, 2]  # Use the generic type variable T
        cmap, norm = mlpColors.from_levels_and_colors(levels=levels, colors=['black', 'red', 'blue'], extend='max')

        ax.scatter(times, final_list, c=colors, s=150, marker='.', edgecolor='none', cmap=cmap, norm=norm, label=labels)

>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93
        plt.xlabel('time(s)')
        plt.grid()
        plt.savefig(path + '_diarization.png')
        plt.show()
<<<<<<< HEAD

    def plot_animation2(self, final_list, path, audio_path):
=======
        return

    def plot_animation2(self, final_list, path):
>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93
        # Load the audio
        import moviepy.editor as mpy
        audio = self.audio
        audio_duration = len(audio)  # / self.SAMPLE_RATE

        # Setup figure and animation parameters
        fig = plt.figure(figsize=(6, 4))

        ax = fig.add_subplot(1, 1, 1)
        repeat_length = 25
        ax.set_xlim([0, repeat_length])
        ax.set_ylim([-0.1, 2.1])
        im, = ax.plot([], [])
        ax.set_title("Speaker Diarization")
        ax.set_xlabel("time(s)")
        ax.set_ylabel("speaker")

        # Define the animation update function
        frames = []

        def update_animation(frame):
            # Calculate the time in seconds for the current frame
            frames.append(frame)
            time = frame / audio_duration

            # Set the animation data
            im.set_xdata(np.arange(frame))
            im.set_ydata(final_list[:frame])

            # Update the x-axis limits based on the current time
            if frame > repeat_length:
                lim = ax.set_xlim(frame - repeat_length, frame)
            else:
                lim = ax.set_xlim(0, repeat_length)

<<<<<<< HEAD
=======
            # Add labels on the top corner
            ax.legend(fontsize='small', title='Speakers:',
                      labels=["No Speaker = 0\nSpeaker 1 = 1\nSpeaker 2 = 2"])
>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93
            return im

        # Calculate the frame duration in milliseconds
        frame_duration = 1000
<<<<<<< HEAD

        # Create the animation
        ani = animation.FuncAnimation(fig, update_animation, frames=int(len(audio)/self.SAMPLE_RATE), interval=frame_duration, blit=False)

        # Remove the legend
        ax.legend().set_visible(False)

        # Add labels on the top corner without the lines
        ax.text(0.95, 0.95, "No Speaker = 0", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
        ax.text(0.95, 0.90, "Interviewer = 1", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
        ax.text(0.95, 0.85, "Interviewee= 2", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')

        # Save the animation as a GIF
        ani.save(path+'_animation2.gif', writer='pillow', fps=30)

        # Save the animation as an MP4 file
        ani.save(path + '_animation2.mp4', writer='ffmpeg', fps=1.0 / frame_duration * 1000)

        mp4_path = path + '_animation2.mp4'
        audio_path = audio_path

        add_audio_to_mp4(mp4_path, audio_path, mp4_path)
=======

        # Create the animations
        ani = animation.FuncAnimation(fig, update_animation, frames=int(len(audio)), interval=frame_duration,
                                      blit=False)

        # Play the audio in the background
        # sd.play(audio, self.SAMPLE_RATE, blocking=False)

        self.play_wav(audio)

        # Display the animation
        plt.show()

        # Save the animation as a GIF
        ani.save(path + 'animation2.gif', writer='pillow')

    def create_vid_from_gif(self, gif_path, out_path):
        import moviepy.editor as mp

        clip = mp.VideoFileClip(gif_path)
        # vid = clip.write_videofile("myvideo.mp4")
        video = clip.set_audio(mp.AudioFileClip(self.wav))
        # fps = 30
        video.write_videofile(out_path)
>>>>>>> 36bfc57dcd94e41db02177bf520df0108761bc93
