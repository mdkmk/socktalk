import argparse
import os
from server_client.start_server_with_ai_client import main as ai_server_main
from server_client.server import main as server_main
from server_client.client import main as client_main
from server_client.terminal_client import main as terminal_client_main


def load_env_variables(filename='.env'):
    try:
        with open(filename) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print("No .env file found, using defaults or command line arguments.")


def main():
    load_env_variables()

    parser = argparse.ArgumentParser(description='Run different parts of the chat application.')
    parser.add_argument('--ai', action='store_true', help='Run the AI server.')
    parser.add_argument('--server', action='store_true', help='Run the server.')
    parser.add_argument('--client', action='store_true', help='Run the client.')
    parser.add_argument('--terminal', action='store_true', help='Run the terminal client.')

    # Optional settings for the AI server
    parser.add_argument('--server_ip_address', type=str, default=os.getenv("SERVER_IP_ADDRESS", "127.0.0.1"),
                        help='IP address of the server')
    parser.add_argument('--server_port', type=int, default=int(os.getenv("SERVER_PORT", 1234)),
                        help='Port number of the server')
    parser.add_argument('--send_full_chat_history', type=lambda x: (str(x).lower() in ['true', '1', 't']),
                        default=os.getenv("SEND_FULL_CHAT_HISTORY", "True") == "True",
                        help='Whether to send full chat history')
    parser.add_argument('--ai_mode1_active', type=lambda x: (str(x).lower() in ['true', '1', 't']),
                        default=os.getenv("AI_MODE1_ACTIVE", "True") == "True", help='Activate mode1 AI')
    parser.add_argument('--ai_mode1_interval', type=int, default=int(os.getenv("AI_MODE1_INTERVAL", 1)),
                        help='Interval for mode1 AI responses')
    parser.add_argument('--ai_mode1_model', type=str, default=os.getenv("AI_MODE1_MODEL", "gpt-3.5-turbo"),
                        help='Model for mode1 AI')
    parser.add_argument('--ai_mode2_active', type=lambda x: (str(x).lower() in ['true', '1', 't']),
                        default=os.getenv("AI_MODE2_ACTIVE", "True") == "True", help='Activate mode2 AI')
    parser.add_argument('--ai_mode2_interval', type=int, default=int(os.getenv("AI_MODE2_INTERVAL", 60)),
                        help='Interval for mode2 AI responses')
    parser.add_argument('--ai_mode2_model', type=str, default=os.getenv("AI_MODE2_MODEL", "gpt-3.5-turbo"),
                        help='Model for mode2 AI')
    parser.add_argument('--ai_mode2_content', type=str,
                        default=os.getenv("AI_MODE2_CONTENT", "Say something interesting from a random Wikipedia page"
                                                              " and start your response with 'Did you know', but don't"
                                                              " mention the source."),
                        help='Content for mode2 AI to initiate conversation')
    parser.add_argument('--openai_api_key', type=str, default=os.getenv('OPENAI_API_KEY', None),
                        help='OpenAI API Key')

    args = parser.parse_args()

    if args.ai:
        if args.openai_api_key:
            os.environ['OPENAI_API_KEY'] = args.openai_api_key

        ai_server_main(server_ip_address=args.server_ip_address,
                       server_port=args.server_port,
                       send_full_chat_history=args.send_full_chat_history,
                       ai_mode1_active=args.ai_mode1_active,
                       ai_mode1_interval=args.ai_mode1_interval,
                       ai_mode1_model=args.ai_mode1_model,
                       ai_mode2_active=args.ai_mode2_active,
                       ai_mode2_interval=args.ai_mode2_interval,
                       ai_mode2_model=args.ai_mode2_model,
                       ai_mode2_content=args.ai_mode2_content)
    elif args.server:
        server_main()
    elif args.client:
        client_main()
    elif args.terminal:
        terminal_client_main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
