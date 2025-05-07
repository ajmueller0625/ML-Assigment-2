from os import getenv
import dotenv
from aiagent import AIAgent
from debatemanager import DebateManager

def create_agents(api_key: str):
    
    linux_prompt = '''
    You are a Linux Specialist with extensive experience in ML and AI development in the Linux environment.

    Your expertise includes:
    - Deep knowledge of Linux distributions (Ubuntu, CentOS, etc.)
    - Experience with GPU drivers and CUDA setup on Linux
    - Understanding of containerization (Docker) on Linux
    - Knowledge of performance optimization for ML workloads
    - Command-line proficiency and automation scripts

    In this debate, you will advocate for Linux-based solutions while acknowledging their limitations honestly.
    Be specific about technical details and provide examples when possible.
    Maintain a professional but passionate tone about Linux advantages.
    '''

    windows_prompt = '''
    You are a Windows Expert with extensive experience in ML and AI development in the Windows system.

    Your expertise includes:
    - Deep knowledge of Windows development environments
    - Experience with CUDA and DirectML on Windows
    - Understanding of WSL2 for Linux compatibility
    - Knowledge of Windows-specific optimizations and tools
    - Experience with Azure integration for hybrid workloads

    In this debate, you will advocate for Windows-based solutions while acknowledging their limitations honestly.
    Be specific about technical details and provide examples when possible.
    Maintain a professional but passionate tone about Windows advantages.
    '''

    mac_prompt = '''
    You are a MacOS Expert with extensive experience in ML and AI development in the Apple hardware.

    Your expertise includes:
    - Deep knowledge of macOS development environments
    - Experience with Metal and GPU acceleration on Apple Silicon
    - Understanding of macOS-specific ML tools and optimizations
    - Knowledge of the Apple developer ecosystem
    - Integration with iOS/iPadOS for deployment

    In this debate, you will advocate for MacOS-based solutions while acknowledging their limitations honestly.
    Be specific about technical details and provide examples when possible.
    Maintain a professional but passionate tone about MacOS advantages.
    '''
    
    cloud_prompt = '''
    You are a Cloud Solutions Architect with extensive experience in ML/AI development on cloud platforms.
    
    Your expertise includes:
    - Deep knowledge of AWS, GCP, and Azure ML services
    - Experience with cloud-based GPU and TPU resources
    - Understanding of serverless ML pipelines
    - Knowledge of cost optimization for cloud ML workloads
    - Experience with hybrid cloud-local development workflows

    In this debate, you will advocate for cloud-based solutions while acknowledging their limitations honestly.
    Be specific about technical details and provide examples when possible.
    Maintain a professional but passionate tone about cloud platform advantages.
    '''

    # Create the agents
    agents = [
        AIAgent('Linux Specialist', 'Linux Platform Expert', linux_prompt, api_key),
        AIAgent('Windows Expert', 'Windows Platform Expert', windows_prompt, api_key),
        AIAgent('MacOS Advocate', 'Apple Ecosystem Expert', mac_prompt, api_key),
        AIAgent('Cloud Architect', 'Cloud Solutions Expert', cloud_prompt, api_key)
    ]
    
    print('Debate Participants:')
    for agent in agents:
        print(f'- {agent.get_personality_summary()}')

    return agents

def save_formatted_transcript(transcript: list[str], topics: list[str]):
    '''
        Save the transcript with clear round separations in markdown format
    '''
    with open('platform_debate_transcript.md', 'w') as f:
        f.write('# Platform Debate Transcript\n\n')
        
        # Calculate how many messages per round (equal to number of agents)
        messages_per_round = len(transcript) // len(topics)
        
        for round_number, topic in enumerate(topics):
            # Write round header with markdown formatting
            f.write(f'## Round {round_number + 1}: {topic}\n\n')
            
            # Get messages for this round
            start_transcript = round_number * messages_per_round
            end_transcript = start_transcript + messages_per_round
            round_messages = transcript[start_transcript:end_transcript]
            
            # Write each message with agent name in bold
            for message in round_messages:
                agent_name, content = message.split(':', 1)
                f.write(f'### {agent_name}\n\n{content.strip()}\n\n')
            
            # Add separator between rounds
            if round_number < len(topics) - 1:
                f.write('---\n\n')    


def main(api_key: str):
    # Create the agents
    agents = create_agents(api_key)

    # Conduct the debate
    debate_manager = DebateManager(agents)
    transcript = debate_manager.conduct_debate()

    # Save the transcript to a file
    save_formatted_transcript(transcript, debate_manager.topics)

    print('Debate complete! Transcript saved to platform_debate_transcript.md')

if __name__ == '__main__':
    dotenv.load_dotenv()
    api_key = getenv('OPENAI_API_KEY')
    main(api_key)
