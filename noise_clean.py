import numpy as np
import soundfile as sf
from sklearn.decomposition import FastICA

MAX_INT = 32767.0


def clear_audio_wiener(in_wav, out_wav='output.wav'):
    from scipy.io import wavfile
    from scipy.signal import wiener

    # Load the audio file
    sample_rate, audio_data = wavfile.read(in_wav)

    # Convert the audio data to float64 format
    audio_data = audio_data.astype(np.float64)

    # Apply a Wiener filter to remove white noise
    filtered_data = wiener(audio_data)

    # Scale the filtered data back to the original data range
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)

    # Save the filtered audio as a new WAV file
    wavfile.write(out_wav, sample_rate, filtered_data)


def clear_audio_librosa(in_wav, out_wav='output.wav'):
    import librosa
    import soundfile as sf

    # Load the audio file
    audio_data, sample_rate = librosa.load(in_wav, sr=None)

    # Compute the magnitude spectrogram
    spec = np.abs(librosa.stft(audio_data))

    # Estimate the noise spectrum
    noise_spec = np.median(spec, axis=1)

    # Set the threshold for noise reduction
    threshold = 1

    # Perform spectral subtraction
    filtered_spec = np.maximum(spec - threshold * noise_spec[:, np.newaxis], 0.0)

    # Reconstruct the audio signal from the modified spectrogram
    filtered_audio = librosa.istft(filtered_spec)

    # Save the filtered audio as a new WAV file
    sf.write(out_wav, filtered_audio, sample_rate)


def final_ica(my_wav):
    audio, sample_rate = sf.read(my_wav)
    ica = FastICA(n_components=10)
    audio_ica = ica.fit_transform(audio)
    num_noise_components = 10
    noise_indices = np.std(audio_ica, axis=0).argsort()[:num_noise_components]
    noise = np.dot(audio_ica[:, noise_indices], ica.components_[noise_indices, :])
    clean_audio = audio - noise
    sf.write('output_wavs/clean_ica.wav', clean_audio, sample_rate)


