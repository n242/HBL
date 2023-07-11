from typing import Iterable, TypeVar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.lines as mlines
from matplotlib import colors as mlpColors
from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp

_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


class Vizualization:
    def __init__(self, wav, sampling_rate, data):
        self.SAMPLE_RATE = sampling_rate
        self.wav = wav
        self.audio = data
        self.times_list = []

    def diarization_for_plot1(self, gen_diarization):
        final_list = []
        max_diar = len(gen_diarization)
        times = np.arange(0, gen_diarization[-1][1], 1)  # arr from 0 to end of audio
        # print(times.shape)
        j = 0
        for i in range(len(times)):
            if j < max_diar:
                if gen_diarization[j][0] < times[i] < gen_diarization[j][1]:
                    if gen_diarization[j][2] == "SPEAKER_00":
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

        color_dict = {
            0: ('black', 'No Speaker'),
            1: ('red', 'Interviewee'),
            2: ('blue', 'Marissa')
        }

        colors = [color_dict[val][0] for val in final_list]
        labels = [color_dict[val][1] for val in final_list]

        black_line = mlines.Line2D([], [], color='black', marker='.', markersize=15, label='No Speaker')
        red_line = mlines.Line2D([], [], color='red', marker='.', markersize=15, label='Interviewee')
        blue_line = mlines.Line2D([], [], color='blue', marker='.', markersize=15, label='Marissa')

        ax.legend(fontsize='small', title='Speakers:', handles=[black_line, red_line, blue_line])

        T = TypeVar('T', int, float)  # Create a generic type variable
        levels: Iterable[T] = [0, 1, 2]  # Use the generic type variable T
        cmap, norm = mlpColors.from_levels_and_colors(levels=levels, colors=['black', 'red', 'blue'], extend='max')

        ax.scatter(times, final_list, c=colors, s=150, marker='.', edgecolor='none', cmap=cmap, norm=norm, label=labels)

        plt.xlabel('time(s)')
        plt.grid()
        plt.savefig(path + 'diarization.png')
        plt.show()
        return

    def plot_animation2(self, final_list, path):
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

            # Add labels on the top corner
            ax.legend(fontsize='small', title='Speakers:',
                      labels=["No Speaker = 0\nSpeaker 1 = 1\nSpeaker 2 = 2"])
            return im

        # Calculate the frame duration in milliseconds
        frame_duration = 1000

        # Create the animations
        ani = animation.FuncAnimation(fig, update_animation, frames=int(len(audio)), interval=frame_duration,blit=False)

        # self.play_wav(audio)
        # plt.show() # Display the animation

        # Save the animation as a GIF
        ani.save(path + 'animation2.gif', writer='pillow')

    def create_vid_from_gif(self, gif_path, out_path):
        # create 2 sec of silence audio segment
        one_sec_segment = AudioSegment.silent(duration=4000)  # duration in milliseconds
        # read wav file to an audio segment
        song = AudioSegment.from_wav(self.wav)
        # Add above two audio segments
        final_song = one_sec_segment + song
        out_audio = "visual_outputs/audio_w_silence.wav"
        final_song.export(out_audio, format="wav")# Either save modified audio

        clip = mp.VideoFileClip(gif_path)
        video = clip.set_audio(mp.AudioFileClip(out_audio))
        video.write_videofile(out_path)

