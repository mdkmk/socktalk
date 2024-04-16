import sys
from server_client.start_server_with_ai_client import main as ai_server_main
from server_client.server import main as server_main
from server_client.client import main as client_main
from server_client.terminal_client import main as terminal_client_main

def main():
    if "--ai" in sys.argv:
        ai_server_main()
    elif "--server" in sys.argv:
        server_main()
    elif "--client" in sys.argv:
        client_main()
    elif "--terminal" in sys.argv:
        terminal_client_main()
    else:
        print("Usage: socktalk --ai | --server | --client")

if __name__ == "__main__":
    main()