import threading
import time
import logging
from .tts import text_to_speech  # Adjust the import based on your package structure

class Timer(threading.Thread):
    def __init__(self, duration, message):
        """
        Initializes the timer.

        Args:
            duration (int): The duration of the timer in seconds.
            message (str): The message to speak when the timer ends.
        """
        super().__init__()
        self.duration = duration
        self.message = message
        self._is_running = True

    def run(self):
        """
        Starts the timer and waits for the specified duration.
        """
        logging.info(f"Timer started for {self.duration} seconds.")
        elapsed = 0
        while elapsed < self.duration and self._is_running:
            time.sleep(1)
            elapsed += 1
        if self._is_running:
            logging.info(f"Timer finished. Speaking message: {self.message}")
            self.speak_message()

    def speak_message(self):
        """
        Uses text_to_speech to speak the message.
        """
        try:
            text_to_speech(self.message)
        except Exception as e:
            logging.error(f"Error in text-to-speech: {e}")

    def stop(self):
        """
        Stops the timer.
        """
        self._is_running = False
        logging.info("Timer stopped.")

# Example usage
if __name__ == "__main__":
    # Start a timer for 10 seconds and speak a message when it ends
    timer = Timer(10, "Check the oven!")  # Message to be spoken when the timer ends
    timer.run()

    # You can stop the timer whenever you want using: timer.stop()
