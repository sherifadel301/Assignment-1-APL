from flask import Flask, render_template_string, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
DATA_FILE = 'users.json'

# Initialize JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Read users from JSON
def read_users():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Write users to JSON
def write_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }

        .content {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            align-items: start;
        }

        @media (max-width: 968px) {
            .content {
                grid-template-columns: 1fr;
            }
        }

        .form-card, .users-card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .form-card h2, .users-card h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 24px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 14px;
        }

        input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.3s ease;
            outline: none;
            background: white;
            color: black;
        }

        input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }

        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-top: 10px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }

        .user-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }

        .user-info {
            margin-bottom: 10px;
            color: black;
        }

        .user-info strong {
            color: #555;
            display: inline-block;
            width: 120px;
        }

        .user-actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .btn-edit, .btn-delete {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s ease;
            width: auto;
        }

        .btn-edit {
            background: #4CAF50;
            color: white;
        }

        .btn-edit:hover {
            background: #45a049;
        }

        .btn-delete {
            background: #f44336;
            color: white;
        }

        .btn-delete:hover {
            background: #da190b;
        }

        .no-users {
            text-align: center;
            color: #999;
            padding: 40px;
        }

        .message {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .btn-cancel {
            background: #666 !important;
            margin-top: 10px;
        }

        .btn-cancel:hover {
            background: #555 !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>User Management System</h1>
            <p>Create, view, edit, and delete users</p>
        </div>

        <div class="content">
            <div class="form-card">
                <h2>{{ 'Edit User' if edit_user else 'Add New User' }}</h2>
                
                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        {% for category, message in messages %}
                            <div class="message {{ category }}">{{ message }}</div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                
                <form method="POST" action="{{ url_for('add_user') if not edit_user else url_for('update_user', user_id=edit_index) }}">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" value="{{ edit_user.username if edit_user else '' }}" required>
                    </div>

                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" name="email" value="{{ edit_user.email if edit_user else '' }}" required>
                    </div>

                    <div class="form-group">
                        <label for="phone">Phone Number</label>
                        <input type="tel" id="phone" name="phone" value="{{ edit_user.phone if edit_user else '' }}" required>
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" value="{{ edit_user.password if edit_user else '' }}" required>
                    </div>

                    <button type="submit">{{ 'Update User' if edit_user else 'Add User' }}</button>
                    
                    {% if edit_user %}
                    <form method="GET" action="{{ url_for('index') }}" style="margin: 0;">
                        <button type="submit" class="btn-cancel">Cancel</button>
                    </form>
                    {% endif %}
                </form>
            </div>

            <div class="users-card">
                <h2>All Users ({{ users|length }})</h2>
                
                {% if users|length == 0 %}
                    <div class="no-users">No users yet. Add one to get started!</div>
                {% else %}
                    {% for user in users %}
                    <div class="user-card">
                        <div class="user-info"><strong>Username:</strong> {{ user.username }}</div>
                        <div class="user-info"><strong>Email:</strong> {{ user.email }}</div>
                        <div class="user-info"><strong>Phone:</strong> {{ user.phone }}</div>
                        <div class="user-info"><strong>Created:</strong> {{ user.created_at }}</div>
                        <div class="user-actions">
                            <form method="GET" action="{{ url_for('edit_user_form', user_id=loop.index0) }}" style="display: inline;">
                                <button type="submit" class="btn-edit">Edit</button>
                            </form>
                            <form method="POST" action="{{ url_for('delete_user', user_id=loop.index0) }}" style="display: inline;" onsubmit="return confirm('Are you sure you want to delete this user?');">
                                <button type="submit" class="btn-delete">Delete</button>
                            </form>
                        </div>
                    </div>
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    users = read_users()
    return render_template_string(HTML_TEMPLATE, users=users, edit_user=None, edit_index=None)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    users = read_users()
    
    new_user = {
        'username': username,
        'email': email,
        'phone': phone,
        'password': password,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    users.append(new_user)
    write_users(users)
    
    flash('User added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:user_id>')
def edit_user_form(user_id):
    users = read_users()
    
    if user_id < 0 or user_id >= len(users):
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template_string(HTML_TEMPLATE, users=users, edit_user=users[user_id], edit_index=user_id)

@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    users = read_users()
    
    if user_id < 0 or user_id >= len(users):
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    users[user_id] = {
        'username': username,
        'email': email,
        'phone': phone,
        'password': password,
        'created_at': users[user_id].get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    }
    
    write_users(users)
    
    flash('User updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    users = read_users()
    
    if user_id < 0 or user_id >= len(users):
        flash('User not found!', 'error')
        return redirect(url_for('index'))
    
    users.pop(user_id)
    write_users(users)
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)