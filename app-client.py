#!/usr/bin/env python3

import socket
import selectors
import libclient

sel = selectors.DefaultSelector()

def create_request(action, value=""):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, value=value),
    )

def start_connection(host, port):
    addr = (host, port)
    print("Connecting to", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, None)
    sel.register(sock, events, data=message)
    return message

def main():
    host, port = "localhost", 65432  # Update with actual server details
    message = start_connection(host, port)
    score = 0

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                if mask & selectors.EVENT_READ:
                    message.read()
                if mask & selectors.EVENT_WRITE:
                    if message.response:
                        # Once response is processed, decide next action
                        if "question" in message.response:
                            user_answer = input("Your answer: ").strip()
                            request = create_request("submit_answer", user_answer)
                        else:
                            print(f"Total score: {score}")
                            request = create_request("get_question")
                        message.request = request
                        message.queue_request()
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("\nExiting game. Goodbye!")
    finally:
        sel.close()

if __name__ == "__main__":
    main()
