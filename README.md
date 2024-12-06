Command Line Trivia Game
========================

This is a multiplayer Command Line Trivia Game implemented in Python, using sockets for client-server communication. Players compete to answer trivia questions correctly, with the game managed by a central server.

**How to Play**
---------------

### **Setup**

1.  **Start the Server**:

    -   Run the `Server.py` script to start the server:

        `python3.8 Server.py -p PORT`

    -   The server will listen for incoming client connections and manage the trivia questions and game state.
2.  **Connect Clients**:

    -   Run the `Client.py` script on different machines or multiple terminals to connect clients to the server:

        `python3.8 Client.py -i SERVER_IP/DNS -p PORT`

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

    `python3.8 Server.py -p <PORT>`

3.  Once all players are connected, type `start` in the server terminal to begin asking trivia questions.
4.  The server will guide the game through all the questions and eventually announce the winner(s).

### **Clients**

1.  Open separate terminals for each player.
2.  Run the client script to join the game:

    `python3.8 Client.py -i <SERVER_IP/DNS> -p <PORT>`

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

-   **`Server.py`**: Runs the server-side of the trivia game, handling client connections, managing questions, tracking scores, and determining the winner.
-   **`Client.py`**: Runs the client-side of the trivia game, allowing players to connect, submit answers, and receive game updates.

**Security Risks**
---------------------

- *No Authentication or Authorization:* The game does not authenticate clients or enforce unique identities, making it vulnerable to impersonation or unauthorized access. *Mitigation:* Implement a secure login system using hashed passwords and session tokens.
- *Input Validation Vulnerabilities:* The game does not validate inputs rigorously, which may lead to injection attacks or unexpected behavior. *Mitigation:* Sanitize and validate all client inputs, especially JSON data, to prevent injection and malformed payloads.
- *Denial of Service (Dos) Risk:* The server could be overwhelmed by a large number of connections or malicious requests, leading to resource exhaustion. *Mitigation:* Implement rate limiting and connection throttling to handle abusive clients.
- *Replay Attacks:* Since there is no mechanism to prevent the reuse of intercepted messages, attackers can replay valid requests. *Mitigation:* Use nonce values or timestamps in messages and enforce strict validation on the server side.
- *Code Injection Risk:* The lack of constraints on inputs such as chat messages could open the game to code injection vulnerabilities. *Mitigation:* Strictly sanitize all user-generated content and use libraries that escape potentially harmful characters.
- *User Enumeration:* The server's feedback for duplicate usernames reveals which usernames are already taken, aiding attackers in user enumeration. *Mitigation:* Return generic error messages that do not disclose this information.

**Roadmap**
---------------------
With this project there is plenty of room for expansion and improvement. A key improvement would be enhancing the user interface from a command-line-based UI to a more modern, interactive web-based UI. This could be done using frameworks like Flask for the backend and React.js for the frontend. This would make the game more visually appealing and accessable. Some other potential changes could be adding different difficulty/levels to the game to allow user to have a challenging or more relaxed way of playing the game. The last potential change I would make going forward would be to add mobile responsiveness or even creating a dedicated mobile app for the game. This would greatly increase the prjects reach and appeal.

**Retrospective**
---------------------
- *What went well:* The project is able to allow for real-time multiplayer gameplay. This is great because it allows multiple clients to connect to the server and play the game simultaniously. The project also has dynamic question handling, sending each question one at a time and waiting for every client to answer before sending the next question. Another thing that went was is the connection management. The project handles client connections and disconnections while leaving the gameplay uninterrupted for the reamaining players.
- *What went wrong:* On my local maching the game was working great and I had everything the way I wanted it to be, but when I had to make it work on the cs120 lab machines I ran into a lot of errors and had to change some aspects of the game that I enjoyed in order to make it run on the lab machines. I probably should have just developed the whole game on the lab machines, that way I would ensure it wouldn't need any changes when it came time for the demos. 
- *Potential improvements:* The error handling and integration testing were kind of rushed on my end, simply because I didn't leave myself enough time to fully ensure a robust game. Another thing that could be improved on is the UI. As of now it's pretty simple and could be made more visually engaging for the user. Also the list of security risks is quite extensive so I believe if I want to take this project any further those would need to be addressed first.