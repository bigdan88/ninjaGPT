import openai
import logging
import utils.audio
import utils.whisper
import utils.tts
import utils.ninjagpt
import pdb

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_api_key(file_path):
    """Read the API key from a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except IOError:
        logging.error("Unable to read API key. Check if the credentials.txt file exists and is readable.")
        return None

# Read API key from credentials.txt
api_key = read_api_key('credentials.txt')
if not api_key:
    logging.critical("API key not found. Exiting.")
    exit(1)

# Initialize OpenAI client with the API key
client = openai.Client(api_key=api_key)

# Main process
logging.info("Starting main process")

# File name for the recorded audio
file_name = "test.wav"

# Record audio and save it to 'file_name'
utils.audio.record_audio(file_name, 0.09, 2)
logging.info("Audio recorded and saved as " + file_name)

# Transcribe the recorded audio
transcription = utils.whisper.transcribe_audio(file_name)
logging.info("Transcription complete")

# Log transcription
logging.info("Transcription: " + transcription)

# Create a ninjaGPT instance and a thread for interaction
ninjaGPT = utils.ninjagpt.create_ninjaGPT(client)
thread = utils.ninjagpt.create_thread(client)
logging.info("ninjaGPT and thread created")

# Use the transcription as a question for ninjaGPT
question = transcription
run = utils.ninjagpt.ask_ninjaGPT(client, thread.id, ninjaGPT.id, question)
logging.info("Question sent to ninjaGPT")

# Wait for ninjaGPT's response to the question
completed_run = utils.ninjagpt.wait_for_run_completion(client, thread.id, run.id)
logging.info("Response received from ninjaGPT")

# Retrieve and log all messages from the thread
messages = utils.ninjagpt.get_thread_messages(client, thread.id)
logging.info("Response: " + messages[0].content[0].text.value)

# Convert the response to speech
utils.tts.text_to_speech(messages[0].content[0].text.value)
logging.info("Text-to-speech conversion completed")

# Uncomment to enable Python Debugger
# pdb.set_trace()
