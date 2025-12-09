Girlfriend Chatbot (demo)

This folder contains a minimal, local demo for storing chats so a chatbot can "remember" past conversations.

What it includes

- bot/store.py  — SQLite-backed ChatStore (save, retrieve, export)
- client/chat_cli.py — Simple CLI that saves user and assistant messages and demonstrates persistence
- tests/test_store.py — Unit tests for ChatStore using unittest

Quick start (requires Python 3.8+)

1. Open a terminal in this folder.
2. Run the CLI: python client/chat_cli.py
3. Commands inside CLI:
   - Type anything to send a message (it will be saved).
   - /show — prints stored conversation for the current user/session
   - /export path.json — export conversation to a JSON file
   - /newsession — start a new session id
   - /exit — quit

Notes

- This is intentionally dependency-free and stores messages in SQLite at `chat_store.db`.
- To integrate an LLM (OpenAI, etc.), replace the simple `generate_reply` function in `client/chat_cli.py` with a call to your model, and continue saving the assistant's messages with `ChatStore.add_message`.
- These conversations are stored locally; be mindful of privacy and data handling when using real personal content.
