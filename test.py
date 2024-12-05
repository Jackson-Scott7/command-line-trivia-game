import unittest
import threading
import socket
import json
import time
from Server import start_server
import logging

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345


class TestTriviaServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.server_thread = threading.Thread(target=start_server, args=(SERVER_HOST, SERVER_PORT), daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give the server some time to start

    def simulate_client(self, messages):
        responses = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            for message in messages:
                client_socket.sendall((json.dumps(message) + "\n").encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8').strip()
                try:
                    parsed_response = json.loads(response)
                    responses.append(parsed_response)
                except json.JSONDecodeError:
                    logging.error(f"Invalid response from server: {response}")
        logging.info(f"Responses received: {responses}")
        return responses


    def test_join_and_broadcast(self):
        # Simulate two clients joining
        client1_messages = [{'type': 'join', 'username': 'Player1'}]
        client2_messages = [{'type': 'join', 'username': 'Player2'}]

        client1_responses = self.simulate_client(client1_messages)
        client2_responses = self.simulate_client(client2_messages)

        self.assertIn('Welcome Player1 to the trivia game!', client1_responses[0]['feedback'])
        self.assertIn('Welcome Player2 to the trivia game!', client2_responses[0]['feedback'])

    def test_question_and_answer(self):
        client_messages = [
            {'type': 'join', 'username': 'Player1'},
            {'type': 'answer', 'username': 'Player1', 'question_id': 'Q1', 'answer': 'Paris'}
        ]

        responses = self.simulate_client(client_messages)
        logging.info(f"Test responses: {responses}")

        # Ensure at least 2 responses (join and answer feedback)
        self.assertGreaterEqual(len(responses), 2, "Expected at least 2 responses")
        self.assertIn('feedback', responses[1], "Feedback key missing in response")
        self.assertIn('Correct!', responses[1]['feedback'])

    def test_invalid_answer(self):
        client_messages = [
            {'type': 'join', 'username': 'Player1'},
            {'type': 'answer', 'username': 'Player1', 'question_id': 'Q1', 'answer': 'London'}
        ]

        responses = self.simulate_client(client_messages)
        logging.info(f"Test responses: {responses}")

        # Ensure at least 2 responses (join and answer feedback)
        self.assertGreaterEqual(len(responses), 2, "Expected at least 2 responses")
        self.assertIn('feedback', responses[1], "Feedback key missing in response")
        self.assertIn('Incorrect!', responses[1]['feedback'])


    def test_quit(self):
        # Simulate a player quitting
        client_messages = [
            {'type': 'join', 'username': 'Player1'},
            {'type': 'quit', 'username': 'Player1'}
        ]

        responses = self.simulate_client(client_messages)

        self.assertIn('Welcome Player1 to the trivia game!', responses[0]['feedback'])

    @classmethod
    def tearDownClass(cls):
        # Cleanup actions (if necessary)
        pass


if __name__ == '__main__':
    unittest.main()
