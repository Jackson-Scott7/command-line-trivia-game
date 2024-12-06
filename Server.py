import socket
import threading
import logging
import json
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)

clients = []
game_state = {
    'current_question_id': None,
    'current_question_text': None,
    'correct_answer': None,
    'scores': {},
    'question_answered': False,
    'answers_received': 0
}

questions = [
    {"id": "Q1", "text": "What is the capital of France?", "answer": "Paris"},
    {"id": "Q2", "text": "What is 5 + 7?", "answer": "12"},
    {"id": "Q3", "text": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
    {"id": "Q4", "text": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"id": "Q5", "text": "What year did the Titanic sink?", "answer": "1912"},
    {"id": "Q6", "text": "What is the chemical symbol for water?", "answer": "H2O"},
    {"id": "Q7", "text": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"}
]

current_question_index = 0

def safe_send(client_socket, message):
    try:
        client_socket.send((message + "\n").encode('utf-8'))
    except BrokenPipeError:
        logging.error(f"Client {client_socket} disconnected unexpectedly.")
        if client_socket in clients:
            clients.remove(client_socket)

def broadcast(message, sender_socket=None):
    for client_socket in clients[:]:
        if client_socket != sender_socket:
            safe_send(client_socket, message)

def broadcast_game_state():
    game_state_message = json.dumps({
        'type': 'game_state',
        'state': {
            'scores': game_state['scores'],
            'current_question': game_state['current_question_text'] if not game_state['question_answered'] else "Question has been answered."
        }
    })
    broadcast(game_state_message)

def handle_join(data, client_socket):
    username = data.get('username')
    if username in game_state['scores']:
        response = json.dumps({
            'type': 'response',
            'feedback': "Username already taken. Please choose a different one."
        })
        safe_send(client_socket, response)
        return

    game_state['scores'][username] = 0
    welcome_message = json.dumps({
        'type': 'response',
        'feedback': f"Welcome {username} to the trivia game!"
    })
    safe_send(client_socket, welcome_message)

    broadcast(json.dumps({
        'type': 'chat',
        'username': 'Server',
        'message': f"{username} has joined the game!"
    }), client_socket)
    broadcast_game_state()

def handle_answer(data, client_socket):
    username = data.get('username')
    question_id = data.get('question_id')
    answer = data.get('answer')

    if not username or not question_id or not answer:
        logging.error("Answer request missing required fields")
        return

    if question_id != game_state['current_question_id']:
        response = json.dumps({
            'type': 'response',
            'correct': False,
            'feedback': "Invalid question ID or no active question."
        })
        safe_send(client_socket, response)
        return

    is_correct = (answer.lower() == game_state['correct_answer'].lower())
    feedback = "Correct!" if is_correct else (f"Incorrect! The correct answer was {game_state['correct_answer']}.")

    if is_correct:
        game_state['scores'][username] += 1

    game_state['answers_received'] += 1

    response = json.dumps({
        'type': 'response',
        'correct': is_correct,
        'feedback': feedback
    })
    safe_send(client_socket, response)

    if game_state['answers_received'] >= len(game_state['scores']):
        game_state['question_answered'] = True
        broadcast_game_state()
        next_question_or_end_game()

def handle_quit(data, client_socket):
    username = data.get('username')
    if username:
        game_state['scores'].pop(username, None)
        broadcast(json.dumps({
            'type': 'chat',
            'username': 'Server',
            'message': f"{username} has left the game."
        }), client_socket)
        clients.remove(client_socket)
        broadcast_game_state()

def next_question_or_end_game():
    global current_question_index
    if current_question_index + 1 < len(questions):
        current_question_index += 1
        send_question_to_all()
    else:
        announce_winner()

def send_question_to_all():
    global current_question_index
    current_question = questions[current_question_index]

    game_state['current_question_id'] = current_question["id"]
    game_state['current_question_text'] = current_question["text"]
    game_state['correct_answer'] = current_question["answer"]
    game_state['question_answered'] = False
    game_state['answers_received'] = 0

    message = json.dumps({
        "type": "start",
        "question": current_question["text"],
        "question_id": current_question["id"]
    })
    broadcast(message)
    broadcast_game_state()

def announce_winner():
    max_score = max(game_state['scores'].values())
    winners = [player for player, score in game_state['scores'].items() if score == max_score]

    if len(winners) == 1:
        winner_message = f"The winner is {winners[0]} with a score of {max_score}!"
    else:
        winner_message = f"It's a tie! The winners are: {', '.join(winners)} with a score of {max_score}!"

    broadcast(json.dumps({
        'type': 'chat',
        'username': 'Server',
        'message': winner_message
    }))
    logging.info(winner_message)

def handle_client(client_socket, client_address):
    logging.info(f"New connection from {client_address}")
    username = None
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if not message:
                break
            data = json.loads(message)
            logging.info(f"Received message from {client_address}: {data}")

            message_type = data.get('type')
            if message_type == 'join':
                username = data.get('username')
                handle_join(data, client_socket)
            elif message_type == 'answer':
                handle_answer(data, client_socket)
            elif message_type == 'quit':
                handle_quit(data, client_socket)
                break
            else:
                logging.error(f"Unknown message type: {message_type}")
    except Exception as e:
        logging.error(f"Error with client {client_address}: {e}")
    finally:
        if username:
            game_state['scores'].pop(username, None)
            broadcast_game_state()
            broadcast(json.dumps({
                'type': 'chat',
                'username': 'Server',
                'message': f"{username} has disconnected from the game."
            }))
        client_socket.close()
        if client_socket in clients:
            clients.remove(client_socket)
        logging.info(f"Connection with {client_address} closed")

def handle_server_commands():
    global current_question_index
    while True:
        command = input("Enter 'start' to send a new question or 'quit' to stop the server: ").strip().lower()
        if command == "start":
            current_question_index = 0
            send_question_to_all()
        elif command == "quit":
            logging.info("Shutting down the server.")
            for client_socket in clients:
                client_socket.close()
            clients.clear()
            exit()
        else:
            logging.warning("Unknown command. Use 'start' or 'quit'.")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    logging.info(f"Server listening on {host}:{port}...")

    threading.Thread(target=handle_server_commands, daemon=True).start()

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the trivia game server.")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to listen on")
    args = parser.parse_args()

    start_server("0.0.0.0", args.port)