import asyncio, websockets, json, sqlite3

DB='backend.db'
clients={}

async def notify_user(username,message):
    ws = clients.get(username)
    if ws:
        try: await ws.send(json.dumps(message))
        except: pass

def store_message(sender,recipient,ciphertext,enc_key,iv):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO messages(sender,recipient,ciphertext,enc_key,iv) VALUES(?,?,?,?,?)",
                 (sender,recipient,ciphertext,enc_key,iv))
    conn.commit(); conn.close()

async def handler(ws):
    username=None
    try:
        async for msg in ws:
            data=json.loads(msg)
            typ=data.get('type')
            if typ=='connect':
                username=data.get('username')
                clients[username]=ws
                print(f"{username} connected")
            elif typ=='send':
                sender=data.get('sender'); rec=data.get('recipient')
                ct=data.get('ciphertext'); ek=data.get('enc_key'); iv=data.get('iv')
                print(f"{sender} sending to {rec}")
                store_message(sender,rec,ct,ek,iv)
                print("message stored")
                await notify_user(rec,{'type':'message','from':sender,'ciphertext':ct,'enc_key':ek,'iv':iv})
    except websockets.ConnectionClosed:
        pass
    finally:
        if username in clients: del clients[username]

async def main():
    print('WebSocket server running on ws://0.0.0.0:6791')
    async with websockets.serve(handler,'0.0.0.0',6791):
        await asyncio.Future()

if __name__=='__main__':
    asyncio.run(main())
