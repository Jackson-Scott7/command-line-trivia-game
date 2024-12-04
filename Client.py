import socket
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)

# Server configurations
HOST = '127.0.0.1'
PORT = 12345

USERNAME = None  # Global variable to store the client's username
game_state = {}  # Store game state locally

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        logging.info(f"Connected to server at {HOST}:{PORT}")
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
                        logging.info(f"New question: {data['question']}")
                        answer_question(client_socket, data['question_id'])
                    
                    elif data['type'] == 'response':
                        feedback = data.get('feedback', "No feedback provided")
                        logging.info(f"Server says: {feedback}")
                    
                    elif data['type'] == 'chat':
                        chat_message = data.get('message', "No message provided")
                        logging.info(f"Chat: {chat_message}")

                    elif data['type'] == 'game_state':
                        update_game_state(data['state'])
                    
                    else:
                        logging.warning(f"Unknown message type: {data['type']}")

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
            'username': USERNAME,  # Use the stored username
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
    client_socket = connect_to_server()
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
