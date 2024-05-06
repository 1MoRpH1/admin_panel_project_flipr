from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from forms import LoginForm, SignupForm
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin, \
    logout_user  # Added logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'FLASK_SECRET_KEY'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/admin_panel_db'
mongo = PyMongo(app)

# Define User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)  # Hash password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Check hashed password

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    user_data = mongo.db.users.find_one({'username': username})
    if user_data:
        return User(user_data['username'], user_data['password'])  # Load hashed password from MongoDB
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists', 'danger')
        else:
            # Hash the password before storing
            hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'password': hashed_password})
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/add_instance', methods=['GET', 'POST'])
@login_required  # Requires authentication to access this route
def add_instance():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        port = request.form.get('port')

        # Save instance information to MongoDB collection
        mongo.db.mongo_instances.insert_one({
            'hostname': hostname,
            'port': port
        })

        flash('MongoDB instance added successfully', 'success')
        return redirect(url_for('dashboard'))  # Redirect to dashboard or any other page

    return render_template('add_instance.html')

@app.route('/dashboard')
@login_required  # Requires authentication to access this route
def dashboard():
    return render_template('dashboard.html', current_user=current_user)  # Pass current_user to the template

@app.route('/logout')
def logout():
    logout_user()  # Perform logout operation
    # Redirect to the login page or any other desired page after logout
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
