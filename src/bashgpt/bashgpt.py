import argparse
import subprocess
import os
import requests
import json


prompt = """
You are an expert bash programmer and are tasked with writing a bash command to perform a given task or answer a question. You must output your response in JSON with a single key 'command' and a value of the bash command you would use to perform the task. Below are the details of your task:
Current Working Directory: {cwd}
Task: {task}
"""

explain_output = """
You are an expert bash programmer and are tasked with explaining the output of a bash command. You must output your response in JSON with a single key 'explanation' and a value of the explanation of the output. Below are the details of your task:
Current Working Directory: {cwd}
Command: {command}
Output: {output}
"""
class InvalidAPIKeyException(Exception):
    pass

def query_openai_chat_gpt4(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",  # Specify the model here
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    # print(response.json())
    if 'error' in response.json():
        if 'Incorrect API key provided' in response.json()['error']['message']:
            raise InvalidAPIKeyException('Incorrect API key provided')
        else:
            raise Exception(response.json()['error']['message'])
    return response.json()['choices'][0]['message']['content']

def construct_bash_command(task, api_key):
    cwd = os.getcwd()   
    prompt = f"""
    You are an expert bash programmer and are tasked with writing a bash command to perform a given task. You must output your response in JSON with a single key 'command' and a value of the bash command you would use to perform the task. Below are the details of your task:
    Current Working Directory: {cwd}
    Task: {task}
    """
    # parse output json
    llm_response = query_openai_chat_gpt4(prompt, api_key)
    llm_response = json.loads(llm_response)
    bash_command = llm_response['command']
    return bash_command

def explain_bash_output(command, output, api_key):
    cwd = os.getcwd()
    prompt = f"""
    You are an expert bash programmer and are tasked with explaining the output of a bash command. You must output your response in JSON with a single key 'explanation' and a value of the explanation of the output. Below are the details of your task:
    Current Working Directory: {cwd}
    Command: {command}
    Output: {output}
    """
    llm_response = query_openai_chat_gpt4(prompt, api_key)
    llm_response = json.loads(llm_response)
    explanation = llm_response['explanation']
    return explanation


def get_api_key(reset):
    api_key_file = 'api_key.txt'
    api_key = None

    # Check if the API key file exists and read the key
    if os.path.isfile(api_key_file):
        with open(api_key_file, 'r') as file:
            api_key = file.read().strip()

    # Ask for the API key if not found
    if not api_key or reset:
        api_key = input("Enter your OpenAI API key: ").strip()
        # Save the API key for future use
        with open(api_key_file, 'w') as file:
            file.write(api_key)

    return api_key

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Python CLI tool to generate and run Bash commands.")
    parser.add_argument('command_description', type=str, help="Text to generate Bash command from.")
    parser.add_argument('--explain', action='store_true', help="Explain the output of the command.")
    parser.add_argument('--reset', action='store_true', help="Reset the API key.")
    args = parser.parse_args()

    # Get or ask for the API key
    api_key = get_api_key(args.reset)



    try:
        bash_command = construct_bash_command(args.command_description, api_key)
    except InvalidAPIKeyException as e:
        print("Invalid API key provided. Please try again.")
        return


    # Show Bash command to user and ask for confirmation
    print("The following Bash command will be executed:\n")
    print(bash_command)
    confirm = input("\nDo you want to execute this command? (y/n): ").strip().lower()

    # Execute the command if confirmed
    if confirm == "y":
        try:
            output = subprocess.run(bash_command, shell=True, check=True, text=True, capture_output=True)
            print("Command output:")
            print(output.stdout)
            if args.explain:
                explanation = explain_bash_output(bash_command, output.stdout, api_key)
                print("Explanation:")
                print(explanation)
        except subprocess.CalledProcessError as e:
            print("Error occurred while executing the command.")
            print(e)
    else:
        print("Command execution cancelled.")

if __name__ == "__main__":
    main()