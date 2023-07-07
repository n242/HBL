from sys import stderr
from time import sleep, perf_counter as timer
from typing import Iterable, TypeVar

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import sounddevice as sd
import matplotlib.lines as mlines
from matplotlib import colors as mlpColors


_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


class Vizualization:
    def __init__(self, wav, sampling_rate, data, data_arr):
        self.SAMPLE_RATE = sampling_rate
        self.wav = wav
        self.audio = data
        self.times_list = []
        self.data_arr = data_arr

    def play_wav(self,  blocking=True):
        try:
            # Small bug with sounddevice.play: the audio is cut 0.5 second too early. so we pad it
            # Convert self.wav to a NumPy array

            data = self.data_arr.astype(np.int16)

            # Concatenate zeros to the waveform
            zeros = np.zeros(self.SAMPLE_RATE // 2, dtype=np.int16)
            data= np.concatenate((data, zeros))

            # Play the audio using sd.play()
            sd.play(data, self.SAMPLE_RATE, blocking=blocking)

        except Exception as e:
            print("Failed to play audio: %s" % repr(e))

    # def diarization_for_plot(self, gen_diarization):
    #     final_list = []
    #     max_diar = len(gen_diarization)
    #     times = np.arange(0, gen_diarization[-1][1], 1)  # arr from 0 to end of audio
    #     #print(times)
    #     j = 0
    #     for i in range(len(times)):
    #         if j < max_diar:
    #             if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
    #                 if gen_diarization[j][2] == "SPEAKER_00":
    #                     final_list.append(0)
    #                 else:
    #                     final_list.append(1)
    #             # elif times[i] > gen_diarization[j][1] and j + 1 < max_diar and times[i] < gen_diarization[j+1][0]:
    #             #     final_list.append(0)
    #             elif times[i]<gen_diarization[j][0]:  # no speaker
    #                 j += 0
    #             else:  # no speaker
    #                 j += 1
    #     self.times_list = final_list
    #     return final_list

    def diarization_for_plot1(self, gen_diarization):
        final_list = []
        max_diar = len(gen_diarization)
        times = np.arange(0, gen_diarization[-1][1], 1)  # arr from 0 to end of audio
        #print(times.shape)
        j = 0
        for i in range(len(times)):
            if j < max_diar:
                if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
                    if gen_diarization[j][2] == "SPEAKER_00":
                        final_list.append(1)
                    else:
                        final_list.append(2)

                elif times[i]>gen_diarization[j][1]: # no speaker
                    final_list.append(0)
                    j += 1
                else:
                    final_list.append(0)
        return final_list


    def plot_diarization(self, final_list, path):
        times = np.arange(0, len(final_list), 1)  # arr from 0 to end of audio

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.suptitle('Speaker Diarization')
        colors = ['black', 'red', 'blue']
        T = TypeVar('T', int, float)  # Create a generic type variable
        levels: Iterable[T] = [0,1,2]  # Use the generic type variable T
        black_line = mlines.Line2D([], [], color='black', marker='.', markersize=15, label='No Speaker')
        red_line = mlines.Line2D([], [], color='red', marker='.', markersize=15, label='Interviewee')
        blue_line = mlines.Line2D([], [], color='blue', marker='.', markersize=15, label='Marissa')

        ax.legend(fontsize='small', title='Speakers:', handles=[black_line, red_line, blue_line])

        cmap, norm = mlpColors.from_levels_and_colors(levels=levels, colors=colors, extend='max')
        timeDiffInt = np.where(np.array(final_list) ==  0, 1,2)
        ax.scatter(times, final_list, c=timeDiffInt, s=150, marker='.', edgecolor='none', cmap=cmap, norm=norm,
                   label=("No Speaker", "Marissa", "Interviewee"))  #
        plt.xlabel('time(s)')
        plt.grid()
        plt.savefig(path + 'diarization.png')
        plt.show()

        return



    # def plot_animation(self, final_list, path):
    #     #data generator
    #     data = np.random.random((100,))
    #
    #     #setup figure
    #     fig = plt.figure(figsize=(5,4))
    #     ax = fig.add_subplot(1,1,1)
    #
    #     #rolling window size
    #     repeat_length = 25
    #
    #     ax.set_xlim([0,repeat_length])
    #     ax.set_ylim([-2,2])
    #
    #
    #     #set figure to be modified
    #     im, = ax.plot([], [])
    #
    #     def func(n):
    #         im.set_xdata(np.arange(n)) # time in secs
    #         im.set_ydata(final_list[0:n])
    #         if n>repeat_length:
    #             lim = ax.set_xlim(n-repeat_length, n)
    #         else:
    #             lim = ax.set_xlim(0,repeat_length)
    #         return im
    #
    #     ani = animation.FuncAnimation(fig, func, frames=data.shape[0], interval=30, blit=False)
    #
    #     plt.show()
    #
    #     ani.save(path+'animation.gif',writer='pillow', fps=30)

    def plot_animation2(self, final_list, path):
        # Load the audio
        audio = self.audio
        audio_duration = len(audio) / self.SAMPLE_RATE

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
        def update_animation(frame):
            # Calculate the time in seconds for the current frame
            time = frame / audio_duration

            # Set the animation data
            im.set_xdata(np.arange(frame))
            im.set_ydata(final_list[:frame])

            # Update the x-axis limits based on the current time
            if frame > repeat_length:
                lim = ax.set_xlim(frame - repeat_length, frame)
            else:
                lim = ax.set_xlim(0, repeat_length)

                # Add labels on the top corner
            # ax.text(0.95, 0.95, "No speaker = -1", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
            # ax.text(0.95, 0.90, "Speaker 1 = 0", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
            # ax.text(0.95, 0.85, "Speaker 2 = 1", transform=ax.transAxes, horizontalalignment='right', verticalalignment='top')
            ax.legend(fontsize='small', title='Speakers:',
                      labels=["No Speaker = 0\nSpeaker 1 = 1\nSpeaker 2 = 2"])


            return im

        # Calculate the frame duration in milliseconds
        frame_duration = 2000

        # Create the animation
        ani = animation.FuncAnimation(fig, update_animation, frames=int(len(audio)/self.SAMPLE_RATE), interval=frame_duration, blit=False)


        # Play the audio in the background
        #sd.play(audio, self.SAMPLE_RATE, blocking=False)

        self.play_wav(audio)

        # Display the animation
        plt.show()

        # Save the animation as a GIF
        ani.save(path+'animation2.gif', writer='pillow', fps=30)

