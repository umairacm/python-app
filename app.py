import os
from flask import Flask, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# --- APPLICATION SETUP ---
app = Flask(__name__)
# IMPORTANT: Generate a good secret key in a real app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_simple_default_secret_key_for_demo') 

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'

# --- USER DATA MANAGEMENT (Simulated Database) ---
# Structure: {'username': {'password': 'hashed_password'}}
USERS = {}

# Add a dummy user for quick testing
USERS['testuser'] = {'password': 'password123'}

# --- USER CLASS FOR FLASK-LOGIN ---
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Function required by Flask-Login to load a user from the session cookie
@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        # Note: In a real app, only store the username in the session cookie (user_id)
        # and fetch the rest of the data from the database here.
        return User(user_id, user_id, USERS[user_id]['password'])
    return None

# --- HTML TEMPLATES AS PYTHON STRINGS ---
# Helper function to generate flash messages container
def get_flashed_messages_html():
    messages_html = ""
    for category, message in app.flashes:
        style = "background-color: #fdd; color: #333; padding: 10px; border: 1px solid #ccc; margin-bottom: 10px;"
        if category == 'success':
            style = "background-color: #dfd; color: #333; padding: 10px; border: 1px solid #ccc; margin-bottom: 10px;"
        elif category == 'info':
            style = "background-color: #ddf; color: #333; padding: 10px; border: 1px solid #ccc; margin-bottom: 10px;"
        
        messages_html += f'<div style="{style}">{message}</div>'
    return messages_html

# --- ROUTES ---

@app.route('/')
def index():
    messages = get_flashed_messages_html()
    
    if current_user.is_authenticated:
        content = f"""
            <p>You are logged in as <strong>{current_user.username}</strong>.</p>
            <p><a href="{url_for('games')}">Continue to Play Games</a></p>
            <p><a href="{url_for('logout')}">Logout</a></p>
        """
    else:
        content = f"""
            <p>You must sign up or log in to play games.</p>
            <p><a href="{url_for('signup')}">Sign Up</a></p>
            <p><a href="{url_for('login')}">Login</a></p>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Home Page</title></head>
    <body style="font-family: Arial;">
        <h1>Welcome to the All-in-One Python Web App!</h1>
        {messages}
        {content}
    </body>
    </html>
    """

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    messages = get_flashed_messages_html()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
             flash('Username and password are required.', 'danger')
             return redirect(url_for('signup'))
        
        if username in USERS:
            flash('Username already taken. Please choose another.', 'danger')
            return redirect(url_for('signup'))

        # In a real app, hash the password (e.g., using bcrypt)
        USERS[username] = {'password': password}
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Sign Up</title></head>
    <body style="font-family: Arial;">
        <h1>Create an Account</h1>
        {messages}
        <form method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Sign Up</button>
        </form>
        <p>Already have an account? <a href="{url_for('login')}">Login here</a>.</p>
    </body>
    </html>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    messages = get_flashed_messages_html()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            user = User(username, username, password)
            login_user(user)
            flash('Successfully logged in!', 'success')
            
            # The next parameter handles redirects after successful login (if applicable)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('games'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Login</title></head>
    <body style="font-family: Arial;">
        <h1>Log In</h1>
        {messages}
        <form method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Log In</button>
        </form>
        <p>Don't have an account? <a href="{url_for('signup')}">Sign up here</a>.</p>
    </body>
    </html>
    """

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/games')
@login_required 
def games():
    """Protected page with game content."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Games</title></head>
    <body style="font-family: Arial;">
        <h1>Welcome, {current_user.username}!</h1>
        <h2>Successfully Logged In!</h2>
        
        <p>This is the exclusive games section. You made it!</p>
        
        <div style="border: 2px solid green; padding: 20px; background-color: #eaffea;">
            <h3>Example Game Content:</h3>
            <ul>
                <li>Game 1: Python Adventure!</li>
                <li>Game 2: Flask Builder</li>
            </ul>
        </div>
        
        <p><a href="{url_for('logout')}">Click here to log out</a>.</p>
        <p><a href="{url_for('index')}">Back to Home</a>.</p>
    </body>
    </html>
    """

# --- RUN THE APPLICATION ---
if __name__ == '__main__':
    print(f"--- All-in-One Flask Demo Running ---")
    print(f"Test user: testuser / password123")
    print(f"Access your application at: http://127.0.0.1:5000/")
    app.run(debug=True)
