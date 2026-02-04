SecureChat Full (Hybrid RSA + AES + WebSocket) - Fixed UI release
----------------------------------------------------------------
Steps to run (Windows):

1. Open PowerShell and go to the project folder
   cd C:\Users\<you>\Downloads\secure_chat_full_ui

2. (Optional) create venv:
   python -m venv .venv
   .venv\Scripts\Activate

3. Install dependencies:
   pip install -r requirements.txt

4. Initialize DB (optional):
   python backend/db_init.py

5. Start Flask backend:
   python backend/app.py

6. Start WebSocket server (in a separate terminal):
   python backend/ws_server.py

7. Open browser and visit:
   http://127.0.0.1:5000/

Notes:
- On signup the client generates RSA keypair and saves private key in localStorage (demo).
- Always load the recipient's public key before sending messages.
- For production use TLS (https/wss) and secure private key storage.
