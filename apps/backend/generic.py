from flask import render_template, session, redirect

@app.route('/dashboard')
def dashboard():
    role = session.get('role')  # Assuming the user's role is stored in the session
    if role == 'donor':
        return render_template('donor/home.html')
    elif role == 'food_bank':
        return render_template('food_bank/home.html')
    elif role == 'volunteer':
        return render_template('volunteer/home.html')
    elif role == 'admin':
        return render_template('admin/home.html')
    else:
        return redirect('/login')
