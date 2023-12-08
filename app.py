from flask import Flask, render_template, request, redirect, url_for, session, flash

import secrets
from db.db import *
from functions.tools import *
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)



@app.route('/')
def index():
    # Check if a user is logged in
    if 'user_id' in session:
        latest_solutions = get_solution()  # Replace with your function to fetch solutions
        
        
        return render_template('home.html', solutions=latest_solutions)

    # User is not logged in, render index.html
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashed_password(request.form['password'])

        
        user_id = signup_db(username, email, password)

        if user_id is not None:
           
            session['user_id'] = user_id

            
            flash('Signup successful!', 'success')
            return redirect(url_for('home'))
        else:
            
            flash('Email or username is already taken. Please choose a different one.', 'error')

    return render_template('signup.html')
#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
       
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

       
        user = query_db('SELECT * FROM user WHERE username = ? AND password_hash = ?', (username, hashed_password(password)), one=True)

        if user:
            # Login successful
            # Set the user ID in the session
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            # Invalid credentials
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        # Connect to the database
        db = get_db()

        # Use a DELETE statement to remove the user with the given user_id
        query = 'DELETE FROM user WHERE id = ?'
        db.execute(query, (user_id,))
        db.commit()

        # Redirect back to the users page after deletion
        return redirect(url_for('view_users'))
    except sqlite3.Error as e:
        # Handle the error (e.g., log it, display a message)
        print(f"Error deleting user: {e}")
        # Redirect back to the users page with an error message
        return redirect(url_for('users', error_message='Error deleting user'))

@app.route('/home')
def home():
    # Retrieve user information from the session or database as needed
    user_id = session.get('user_id')
    # Add logic to fetch additional user data if necessary
    sol=get_solution()
    return render_template('home.html', user_id=user_id,sol=sol)

@app.route('/submit_solution', methods=['POST'])
def submit_solution():
    if request.method == 'POST':
        # Get form data
        problem_id = request.form['problem_id']
        user_id = session.get('user_id')
        solution_description = request.form['solution_description']
        language = request.form['language']
        github_link = request.form['github_link']

        # Process the form data and save it to the solutions table in the database
        save_solution_to_db(problem_id, user_id, solution_description, language, github_link)
        sol=get_solution()
        # Redirect to the home page or any other page after form submission
        return redirect(url_for('home'),sol=sol)

    # If the request method is not POST, redirect to the home page
    flash("error")
    return redirect(url_for('submit_solution'))

@app.route('/submit_solution_page')
def submit_solution_page():
    problems = get_problem()  # Replace with your function to fetch problems from the database
    return render_template('submit_solution.html', problems=problems)


@app.route('/users')
def view_users():
    users = query_db('SELECT * FROM solutions')
    return render_template('users.html', users=users)





if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    app.run(debug=True)
