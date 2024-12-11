from flask import Flask, render_template, request, redirect,url_for, flash, session
from flask_socketio import SocketIO, send, emit
import socket
import os
from datetime import datetime
import pytz
from flask import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test environment'
socketio = SocketIO(app)

USER_FILE = 'users.txt'

# Example server-side code to send timestamp
timestamp = datetime.utcnow().isoformat()

def load_users():
    try:
        # Open the user file in read mode
        with open(USER_FILE,'r') as file:
            users = file.readlines()
            
        # Process each line into a dictionary    
        return [{'id': int(user.split(',')[0]), 'username':user.split(',')[1].strip(), 'password':user.split(',')[2].strip()} for user in users]
    except FileNotFoundError: # Return an empty list if the file is not found

        return[]

def save_user(user_id,username,password):
    with open(USER_FILE,'a') as file:
        file.write(f"{user_id},{username},{password}\n")
        
@app.route('/')
def index():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user['username'] == username for user in users):
            flash('Username already exists. Please choose another')
            return redirect(url_for('register'))
        user_id = len(users) + 1
        save_user(user_id, username, password)
        flash('Account created successfully. Please login')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(msg):
    username = session.get('username')
    timezone = pytz.timezone('Asia/Manila')  # Use your desired timezone
    timestamp = datetime.now(timezone).isoformat()

  
    if username:
        print(f"{username}:{msg}")
        send({'msg':msg, 'username': username, 'timestamp': timestamp}, broadcast=True)
        

# @app.route('/')
# def index():
#     return render_template('chat.html')

if __name__ == '__main__':
    socketio.run(app,debug=True)