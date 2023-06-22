from sys import stderr
from time import sleep, perf_counter as timer
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

import matplotlib.lines as mlines
from matplotlib import colors as mlpColors

_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


class Vizualization:
    def __init__(self, wav, sampling_rate):
        self.SAMPLE_RATE = sampling_rate
        self.wav = wav

    def play_wav(self, blocking=True):
        try:
            import sounddevice as sd
            # Small bug with sounddevice.play: the audio is cut 0.5 second too early. We pad it to
            # make up for that
            self.wav = np.concatenate((self.wav, np.zeros(self.SAMPLE_RATE // 2)))
            sd.play(self.wav, self.SAMPLE_RATE, blocking=blocking)
        except Exception as e:
            print("Failed to play audio: %s" % repr(e))

    def diarization_for_plot(self, gen_diarization):
        final_list = []
        max_diar = len(gen_diarization)
        times = np.arange(0, gen_diarization[-1][1], 1)  # arr from 0 to end of audio
        j = 0
        for i in range(len(times)):
            if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
                if gen_diarization[j][2] == "SPEAKER_00":
                    final_list.append(1)
                else:
                    final_list.append(2)
            if times[i] >gen_diarization[j][1] and j< max_diar and times[i] <gen_diarization[j+1][0]:
                final_list.append(0)
            else:  # no speaker
                j += 1

        return final_list


    """
    I get the following error:  in diarization_for_plot
    if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
IndexError: list index out of range
    """

    def plot_diarization(self, final_list):
        print("inside plotting")
        times = np.arange(0, len(final_list), 1)  # arr from 0 to end of audio

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.suptitle('Speaker Diarization')
        colors = ['black', 'red', 'blue']
        levels = [0, 1, 2]
        blue_line = mlines.Line2D([], [], color='blue', marker='.', markersize=15, label='Marissa')
        red_line = mlines.Line2D([], [], color='red', marker='.', markersize=15, label='Interviewee')
        ax.legend(fontsize='small', title='Speakers:', handles=[blue_line, red_line])

        cmap, norm = mlpColors.from_levels_and_colors(levels=levels, colors=colors, extend='max')
        timeDiffInt = np.where(np.array(final_list) == 0, 1, 2)
        ax.scatter(times, final_list, c=timeDiffInt, s=150, marker='.', edgecolor='none', cmap=cmap, norm=norm,
                   label=("No Speaker", "Marissa", "Interviewee"))  #
        plt.xlabel('time(s)')
        plt.grid()
        plt.show()
        plt.savefig('diarization.png')

        return

    def plot_animation(self, final_list):
        #data generator
        data = np.random.random((100,))

        #setup figure
        fig = plt.figure(figsize=(5,4))
        ax = fig.add_subplot(1,1,1)

        #rolling window size
        repeat_length = 25

        ax.set_xlim([0,repeat_length])
        ax.set_ylim([-2,2])


        #set figure to be modified
        im, = ax.plot([], [])

        def func(n):
            im.set_xdata(np.arange(n)) # time in secs
            im.set_ydata(final_list[0:n])
            if n>repeat_length:
                lim = ax.set_xlim(n-repeat_length, n)
            else:
                lim = ax.set_xlim(0,repeat_length)
            return im

        ani = animation.FuncAnimation(fig, func, frames=data.shape[0], interval=30, blit=False)

        plt.show()

        ani.save('animation.gif',writer='pillow', fps=30)
