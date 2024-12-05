import socket
import logging
import json
import argparse
from colorama import Fore, Style

# Set up logging
logging.basicConfig(level=logging.INFO)

USERNAME = None  # Global variable to store the client's username
game_state = {}  # Store game state locally

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        logging.info(f"Connected to server at {host}:{port}")
        return client_socket
    except Exception as e:
        logging.error(f"Failed to connect to server: {e}")
        return None

def send_message(client_socket, message_data):
    message = json.dumps(message_data)
    client_socket.send((message + "\n").encode('utf-8'))

def handle_response(client_socket):
    buffer = ""
    while True:
        try:
            buffer += client_socket.recv(1024).decode('utf-8')
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if message:
                    data = json.loads(message)

                    if data['type'] == 'start':
                        # New questions in green
                        print(f"{Fore.CYAN}New question: {data['question']}{Style.RESET_ALL}")
                        answer_question(client_socket, data['question_id'])

                    elif data['type'] == 'response':
                        feedback = data.get('feedback', "No feedback provided")
                        if data.get('correct') is True:
                            # Correct answers displayed in green
                            print(f"{Fore.GREEN}Server says: {feedback}{Style.RESET_ALL}")
                        elif data.get('correct') is False:
                            # Incorrect answers displayed in red
                            print(f"{Fore.RED}Server says: {feedback}{Style.RESET_ALL}")
                        else:
                            # Neutral feedback in default color
                            print(f"Server says: {feedback}")

                    elif data['type'] == 'chat':
                        chat_message = data.get('message', "No message provided")
                        if "has left the game" in chat_message or "disconnected" in chat_message:
                            # Player disconnection messages in red
                            print(f"{Fore.YELLOW}Chat: {chat_message}{Style.RESET_ALL}")
                        else:
                            print(f"Chat: {chat_message}")

                    elif data['type'] == 'game_state':
                        update_game_state(data['state'])

                    else:
                        print(f"Unknown message type: {data['type']}")

        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            break

def answer_question(client_socket, question_id):
    while True:
        answer = input(f"Enter your answer for question {question_id} (or type 'quit' to leave): ")
        if answer.strip().lower() == "quit":
            send_quit_message(client_socket)
            return
        send_message(client_socket, {
            'type': 'answer',
            'username': USERNAME,
            'question_id': question_id,
            'answer': answer
        })
        break

def send_quit_message(client_socket):
    send_message(client_socket, {'type': 'quit', 'username': USERNAME})
    logging.info("You have left the game.")
    client_socket.close()
    exit()

def update_game_state(state):
    global game_state
    game_state = state
    print("\n--- Game State ---")
    print("Scores:")
    for player, score in state['scores'].items():
        print(f"  {player}: {score}")
    print("------------------")
    current_question = state.get('current_question', 'No question available')
    if current_question and current_question != "Question has been answered.":
        print(f"Current Question: {current_question}")
    else:
        print(current_question)
    print("------------------\n")

def main():
    global USERNAME

    parser = argparse.ArgumentParser(description="Connect to the trivia game server.")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server IP or DNS")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    args = parser.parse_args()

    client_socket = connect_to_server(args.ip, args.port)
    if client_socket:
        while True:
            USERNAME = input("Enter your username: ")
            send_message(client_socket, {'type': 'join', 'username': USERNAME})
            response = client_socket.recv(1024).decode('utf-8').strip()
            data = json.loads(response)
            if "already taken" not in data.get('feedback', ''):
                break
            print(data.get('feedback'))
        handle_response(client_socket)

if __name__ == "__main__":
    main()
