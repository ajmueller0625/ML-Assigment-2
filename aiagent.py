from openai import OpenAI

class AIAgent:
    def __init__(self, name: str, personality: str, prompt: str, key: str):
        self.name = name
        self.personality = personality
        self.history = [{'role': 'system', 'content': prompt}]
        self.client = OpenAI(api_key=key)
        
    def _add_message(self, message: str, role: str):
        '''
        Add a message to the history.
        '''
        self.history.append({'role': role, 'content': message})

    def get_personality_summary(self):
        '''
        Get a summary of the personality of the AI agent.
        '''
        return f'{self.name} : {self.personality}'

    def generate_response(self, prompt: str = None):
        '''
        Generate a response from the AI agent.
        If a prompt is provided, it will be added to the history.
        '''
        if prompt:
            self._add_message(prompt, 'user')

        # Generate a response from the AI agent using the OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            max_tokens=800, # Maximum number of tokens in the response
            temperature=0.7 # Temperature for the response to make it more or less random
        )
        
        # Get the response content from the OpenAI API
        response_content = response.choices[0].message.content
        self._add_message(response_content, 'assistant')
        
        return response_content
        

        
