# Chat Server

If running the code from the github repository:
Please install the requirements into a virtual environment, then launch "start_server_with_ai_client.py" after adjusting the settings (send full chat history, ai client api key, enabling ai mode 1 or ai mode 2, editing mode1 or mode2 intervals), then launch "client.py" (can be launched multiple times, for multiple users)

If running the code using the python library "socktalk" (pip install socktalk):
You can use the following terminal commands:
1) "ai_server": Runs the chat server with a connected AI client. Currently uses gpt-3.5-turbo model.
    You should create an environment file named ".env" in the working directory from which you execute the python
    commands for the library, in order to adjust the AI modes and chat server settings.

    Below is an example for your .env file. You will need to update the OpenAI chatgpt API key. In order for the API key to function you will need to load at least 5$ of credit on your OpenAI account.
    The AI client has two modes which can be toggled on or off using "True" or "False". AI response intervals can be adjusted. See below for more details.

    ### ".env" file example
    
    OPENAI_API_KEY=<OPENAI_API_KEY_HERE>

    SERVER_IP_ADDRESS=127.0.0.1

    SERVER_PORT=1234

    SEND_FULL_CHAT_HISTORY=True

    AI_MODE1_ACTIVE=True

    AI_MODE1_INTERVAL=1

    AI_MODE2_ACTIVE=True

    AI_MODE2_INTERVAL=60


2) "chat_server": Runs a chat server without a connected AI client. No .env file necessary.


3) "chat_client": Runs the user chat client.


## Python Networking Task: Building a Chat Server and Client

Your task is to build a simple chat system using Python. The system will consist of a server and a client. Multiple clients should be able to connect to the server, send messages, and receive messages from other clients.

Server

The server should be able to handle multiple clients concurrently. It should be able to receive a message from a client and broadcast it to all other connected clients. The server should use non-blocking sockets and select.select() to handle multiple connections.

Client

The client should be able to connect to the server, send messages, and receive messages from other clients. The client should be able to send and receive messages concurrently. You can use threading to handle sending and receiving messages concurrently.

Message Protocol

The server and client should use a simple protocol for messages. Each message should start with a fixed-length header that contains the length of the actual message. This way, the server knows when it has received the full message. The client should follow this protocol when sending messages.

Requirements

The server should be able to handle multiple clients concurrently.
The client should be able to send and receive messages concurrently.
The server should broadcast incoming messages to all connected clients.
The client and server should use a simple protocol for messages.

AI Client

The AI client will connect to the server and respond to the chat. It has two modes:
1. Respond every N lines: the bot reads the conversation and responds to the conversation once every N lines
2. ⁠Respond every N seconds: the bot says something completely new and unrelated every N seconds



