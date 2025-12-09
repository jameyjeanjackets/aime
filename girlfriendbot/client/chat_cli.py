import uuid
import argparse
import os
import sys
from bot.store import ChatStore


def generate_reply(user_message):
    """Placeholder reply generator. Replace this with a real LLM call.

    Keep it simple: reflect back with a loving tone.
    """
    # Very simple persona-like reply
    return f"I hear you: \"{user_message}\" — that matters to me. 💕"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user_1', help='user id (default user_1)')
    parser.add_argument('--db', default=None, help='path to sqlite db (optional)')
    args = parser.parse_args()

    user_id = args.user
    session_id = str(uuid.uuid4())[:8]
    store = ChatStore(db_path=args.db)

    print(f"Starting chat CLI for user={user_id}, session={session_id}")
    print("Type messages and press Enter. Commands: /show, /export <path>, /newsession, /exit")

    while True:
        try:
            txt = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting...')
            break

        if not txt:
            continue

        if txt.startswith('/'):
            cmd_parts = txt.split(maxsplit=1)
            cmd = cmd_parts[0].lower()
            arg = cmd_parts[1] if len(cmd_parts) > 1 else None
            if cmd == '/show':
                conv = store.get_conversation(user_id, session_id)
                if not conv:
                    print('(no messages yet)')
                for m in conv:
                    who = 'You' if m['role'] == 'user' else 'GF'
                    print(f"[{m['timestamp']}] {who}: {m['content']}")
            elif cmd == '/export':
                path = arg or f'conv_{user_id}_{session_id}.json'
                out = store.export_conversation(user_id, session_id, path=path)
                print(f'Exported to {out}')
            elif cmd == '/newsession':
                session_id = str(uuid.uuid4())[:8]
                print(f'New session: {session_id}')
            elif cmd == '/exit':
                print('Goodbye')
                break
            else:
                print('Unknown command')
            continue

        # Save user message
        store.add_message(user_id, session_id, 'user', txt)

        # Generate assistant reply (placeholder)
        reply = generate_reply(txt)

        # Save assistant message
        store.add_message(user_id, session_id, 'assistant', reply)

        # Print reply
        print('GF: ' + reply)


if __name__ == '__main__':
    main()
