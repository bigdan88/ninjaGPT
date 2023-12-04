# Filename: chatgpt_api.py
import openai
import logging
import pdb

class ChatGPTAPI:
    def __init__(self, api_key):
        """
        Initialize the ChatGPT API client.

        Args:
            api_key (str): The API key for accessing OpenAI's Chat Completions API.
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.messages = []

    def add_system_message(self, content):
        """
        Adds a system message to set the behavior of the assistant.

        Args:
            content (str): The content of the system message.
        """
        self.messages.append({"role": "system", "content": content})

    def ask_question(self, question):
        """
        Sends a question to the ChatGPT API, appends it to the conversation history, 
        retrieves the response, and appends the response to the conversation history.

        Args:
            question (str): The question to be asked.

        Returns:
            str: The response from ChatGPT.
        """
        # Append the user question to the conversation history
        self.messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=self.messages
            )
            # Extract the assistant's response
            # Accessing the response using the correct object attribute
            assistant_message = response.choices[0].message.content

            # Append the assistant's response to the conversation history
            self.messages.append({"role": "assistant", "content": assistant_message})

            return assistant_message
        except Exception as e:
            logging.error("Error in ChatGPT API request: " + str(e))
            return ""


    def get_conversation_history(self):
        """
        Returns the current conversation history.

        Returns:
            list: The conversation history.
        """
        return [msg['content'] for msg in self.messages if msg['role'] in ['user', 'assistant']]

# Example usage
if __name__ == "__main__":
    api_key = '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'  # Replace with your actual OpenAI API key
    chat_gpt = ChatGPTAPI(api_key)
    chat_gpt.add_system_message("You are a helpful assistant.")  # Optional system message
    response = chat_gpt.ask_question("What is the capital of France?")
    print("Response:", response)
    print("\nConversation History:")
    print("\n".join(chat_gpt.get_conversation_history()))
