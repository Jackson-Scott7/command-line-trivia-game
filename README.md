Command Line Trivia Game
========================

This is a multiplayer Command Line Trivia Game implemented in Python, using sockets for client-server communication. Players compete to answer trivia questions correctly, with the game managed by a central server.

**How to Play**
---------------

### **Setup**

1.  **Start the Server**:

    -   Run the `server.py` script to start the server:

        `python server.py`

    -   The server will listen for incoming client connections and manage the trivia questions and game state.
2.  **Connect Clients**:

    -   Run the `client.py` script on different machines or multiple terminals to connect clients to the server:

        `python client.py`

    -   Each client will be prompted to enter a unique username to join the game.
    -   Multiple clients (players) can join before starting the game.
3.  **Start the Game**:

    -   After all players have connected, enter `start` on the server console to begin the game.
    -   The game will ask a total of 7 trivia questions, one at a time.

### **Gameplay**

-   **Question Rounds**:

    -   Each round, the server broadcasts a trivia question to all connected clients.
    -   All players answer the question simultaneously.
    -   Players submit their answers through their client terminals.
-   **Scoring**:

    -   Players receive feedback immediately after submitting an answer.
    -   Correct answers earn players points.
    -   The current scores of all players are displayed after each question, helping everyone keep track of the competition.
-   **Next Question**:

    -   After all connected players have answered the current question, the server will move on to the next question.
    -   This continues until all 7 questions have been asked.
-   **Winning**:

    -   At the end of the game, the server announces the winner(s).
    -   If there is a tie, all winning players are displayed.

### **Game Features**

-   **Simultaneous Answering**:

    -   Unlike a turn-based trivia game, all players answer each question at the same time.
-   **Real-Time Game State Synchronization**:

    -   The server maintains the game state and broadcasts updates to all clients.
    -   Player scores are prominently displayed, and the current question is shown separately for clarity.
-   **Client Disconnection Handling**:

    -   Players can leave the game at any point by typing `quit`. The server will notify all other players of the disconnection.
-   **Winner Announcement**:

    -   After all questions are completed, the server determines and announces the winner(s) based on scores.

**Technologies Used**
---------------------

-   **Python**: Core language used to develop the trivia game.
-   **Sockets**: Python's `socket` library is used to manage communication between the server and clients.

**How to Run**
--------------

### **Server**

1.  Open a terminal.
2.  Run the server script to start the game:

    `python server.py`

3.  Once all players are connected, type `start` in the server terminal to begin asking trivia questions.
4.  The server will guide the game through all the questions and eventually announce the winner(s).

### **Clients**

1.  Open separate terminals for each player.
2.  Run the client script to join the game:

    `python client.py`

3.  Each player will be prompted to enter a unique username.
4.  Players will receive questions from the server and can answer them directly in the terminal.



**Requirements**
----------------

-   Python 3.x

**Additional Resources**
------------------------

-   [Python Documentation](https://docs.python.org/3/)
-   [Socket Programming in Python](https://docs.python.org/3/library/socket.html)

**Project Structure**
---------------------

-   **`server.py`**: Runs the server-side of the trivia game, handling client connections, managing questions, tracking scores, and determining the winner.
-   **`client.py`**: Runs the client-side of the trivia game, allowing players to connect, submit answers, and receive game updates.