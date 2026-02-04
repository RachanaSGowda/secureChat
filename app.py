from flask import Flask, request, jsonify, send_from_directory
import sqlite3, hashlib, os
from db_init import init_db

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
DB_PATH = 'backend.db'
if not os.path.exists(DB_PATH):
    init_db(DB_PATH)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    public_key = data.get('public_key')
    if not username or not password or not public_key:
        return jsonify({'error':'missing'}),400
    ph = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('INSERT OR REPLACE INTO users(username,password_hash,public_key) VALUES(?,?,?)',(username,ph,public_key))
        conn.commit()
        return jsonify({'status':'ok'})
    except Exception as e:
        return jsonify({'error':'failed'}),400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username'); password = data.get('password')
    ph = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db(); cur = conn.cursor()
    cur.execute('SELECT username,public_key FROM users WHERE username=? AND password_hash=?',(username,ph))
    row = cur.fetchone(); conn.close()
    if row:
        return jsonify({'status':'ok','username':row['username'],'public_key':row['public_key']})
    return jsonify({'error':'invalid'}),401

@app.route('/public_key/<username>')
def get_public_key(username):
    conn = get_db(); cur = conn.cursor()
    cur.execute('SELECT public_key FROM users WHERE username=?',(username,))
    row = cur.fetchone(); conn.close()
    if not row:
        return jsonify({'error':'notfound'}),404
    return jsonify({'public_key':row['public_key']})

@app.route('/')
def index():
    return send_from_directory('../frontend','index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

if __name__=='__main__':
    app.run(debug=True)
