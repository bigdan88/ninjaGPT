import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(filename="recording.wav", threshold=0.09, timeout=2):
    """
    Records audio from the microphone and saves it to a file.
    Stops recording when silence is detected.

    Args:
        filename (str): The name of the file where the audio will be saved.
        threshold (float): The silence threshold.
        timeout (int): The timeout in seconds for silence detection.
    """

    # Set the audio recording parameters
    samplerate = 44100  # Sample rate in Hertz
    duration = 3  # Duration for each recording segment in seconds
    channels = 1  # Number of audio channels

    # Function to check for silence
    def is_silent(data, threshold):
        """Check if the given data is below the silence threshold."""
        return np.all(np.abs(data) < threshold)

    logging.info("Recording started. Speak into the microphone. Stop speaking to end recording.")
    
    # Start recording in chunks and check for silence
    recorded_data = []
    silent_segments = 0
    while True:
        data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='float64')
        sd.wait()  # Wait until recording is finished
        recorded_data.append(data)

        if is_silent(data, threshold):
            silent_segments += 1
        else:
            silent_segments = 0

        if silent_segments >= timeout:
            break

    # Concatenate all recorded chunks
    recorded_data = np.concatenate(recorded_data, axis=0)

    # Save the recording as a WAV file
    write(filename, samplerate, recorded_data)
    logging.info(f"Recording saved as {filename}")

if __name__ == "__main__":
    record_audio()
