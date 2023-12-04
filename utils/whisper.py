import openai
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_api_key(file_path):
    """
    Reads the API key from a file.

    Args:
        file_path (str): Path to the file containing the API key.

    Returns:
        str: The API key.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except IOError:
        logging.error("Unable to read API key. Check if the credentials file exists and is readable.")
        return None

# Read API key from credentials file
api_key = read_api_key('credentials.txt')
if not api_key:
    logging.critical("API key not found. Exiting.")
    exit(1)

# Initialize OpenAI client with the API key
client = openai.Client(api_key=api_key)

def transcribe_audio(file_path):
    """
    Transcribes the audio file at the given path using OpenAI's audio transcriptions API.

    Args:
        file_path (str): The path to the audio file to transcribe.

    Returns:
        str: The transcribed text.
    """

    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        logging.info("Audio transcription completed for " + file_path)
        return transcription.text  # Accessing the text attribute directly
    except Exception as e:
        logging.error("Failed to transcribe audio: " + str(e))
        return ""

if __name__ == "__main__":
    # Example usage
    file_path = "test.wav"  # Replace with your actual file path
    transcription = transcribe_audio(file_path)
    logging.info("Transcription: " + transcription)
