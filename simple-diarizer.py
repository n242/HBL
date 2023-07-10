from simple_diarizer.diarizer import Diarizer
from simple_diarizer.utils import (waveplot, combined_waveplot)


import matplotlib.pyplot as plt
import soundfile as sf


NUM_SPEAKERS = 2 # The number of speakers

def run_simple_diarizer():
    wav_file = "combined_vid1.wav"
    signal, fs = sf.read(wav_file)

    print(f"wav file: { wav_file}")

    diar = Diarizer(
        embed_model='ecapa',  # supported types: ['xvec', 'ecapa']
        cluster_method='sc',  # supported types: ['ahc', 'sc']
        window=1.5,  # size of window to extract embeddings (in seconds)
        period=0.75  # hop of window (in seconds)
    )

    # If using NUM_SPEAKERS
    segments = diar.diarize(wav_file,
                            num_speakers=NUM_SPEAKERS,
                            outfile=f"1.rttm")

    waveplot(signal, fs, figsize=(20,3))
    plt.show()

    combined_waveplot(signal, fs, segments, figsize=(10,3), tick_interval=60)
    plt.show()

if __name__ == '__main__':
    run_simple_diarizer()