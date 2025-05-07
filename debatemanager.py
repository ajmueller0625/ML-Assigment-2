from aiagent import AIAgent


class DebateManager:
    def __init__(self, agents:list[AIAgent]):
        '''
        Initialize the debate manager with a list of agents
        Args:
            agents: list of AIAgent objects
        '''
        self._agents = {agent.name: agent for agent in agents}
        self._history_transcript = []
        self._round = 0
        self.topics = [
            "Initial platform advocacy",
            "GPU acceleration and compute requirements", 
            "Development environment setup",
            "Software compatibility for ML frameworks",
            "Cost considerations",
            "Performance benchmarks for ML workloads",
            "Local vs. cloud trade-offs",
            "Final recommendations"
        ]

    def _add_transcript(self, message: str, agent_name: str):
        '''
        Add a message to the transcript
        Args:
            message: str
            agent_name: str
        '''
        self._history_transcript.append(f'{agent_name}: {message}')

    def _get_context(self, round_number: int):
        '''
        Create the context for the current round
        Args:
            round_number: int

        Returns:
            Relevant transcript history/entries as a joined string
        '''
        if round_number == 0:
            return 'This is the first round of the debate.'

        # Create a list to store the context for the current round
        context = []
        for round in range(round_number):
            topic = self.topics[round]
            context.append(f'Round {round + 1} - {topic}')

            # Get the relevant transcript history/entries for the current round
            start_transcript = round * len(self._agents)
            end_transcript = (round + 1) * len(self._agents)
            round_messages = self._history_transcript[start_transcript:end_transcript]

            # Save the transcript history/entries for this round
            for message in round_messages:
                context.append(message)

        return '\n'.join(context)

    def _conduct_round(self, round_number: int):
        '''
        Conduct a round of the debate
        Args:
            round_number: int

        Returns:
            A dictionary of responses from the agents
        '''
        # Get the current topic from the list
        current_topic = self.topics[round_number]
        print(f'Round {round_number + 1} - {current_topic}')

        # Get the relevant context for the round from the transcript
        context = self._get_context(round_number)

        responses = {}
        for name, agent in self._agents.items():

            if current_topic == 'Final recommendations':
                prompt = f'''
                Current debate round: {round_number + 1}
                Topic: {current_topic}
                    
                Previous discussion summary:
                {context}
                
                This is the final round of the debate. As the {name}, provide your FINAL RECOMMENDATION 
                for the optimal computing platform setup for a student taking an ML+AI course.
                
                Your recommendation should:
                1. Clearly state which platform(s) you believe are best suited for the course requirements
                2. Summarize the key advantages of your recommended approach
                3. Acknowledge any limitations and how they might be addressed
                4. Consider potential hybrid approaches if appropriate
                5. Focus on practical, actionable advice for students
                
                Be concise but technically accurate in your final recommendation.
                '''
            else:
                prompt = f'''
                Current debate round: {round_number + 1}
                Topic: {current_topic}
                
                Previous discussion summary:
                {context}
                
                As the {name}, provide your perspective on this topic. 
                Focus specifically on how your platform addresses this aspect for ML/AI coursework.
                Be concise but technically accurate. You may respond to points made by other experts.
            '''

            response = agent.generate_response(prompt)
            responses[name] = response
            self._add_transcript(response, name)

        self._round += 1

        return responses
    
    def conduct_debate(self):
        '''
            Conduct the entire debate
        '''
        for round_number in range(len(self.topics)):
            self._conduct_round(round_number)

        return self._history_transcript