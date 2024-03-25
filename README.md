# Chat Server

Please install the requirements, and if you run into issues you can use a virtual environment, then launch either start_server_with_ai_client_v3.py after adjusting the settings (ai_client api key, enabling ai mode 1 or ai mode 2), then launch ai_client_v5.py (can be launched multiple times, for multiple users)

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



