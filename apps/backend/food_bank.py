from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database'
}

@app.route('/foodbank')
def foodbank():
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to fetch donor data
    query = """
        SELECT d.name, d.address, d.contact, f.quantity, f.food_type
        FROM donor d
        JOIN food f ON d.donor_id = f.donor_id
    """
    cursor.execute(query)
    donors = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('foodbank.html', donors=donors)
@app.route('/order.html')
def order_page():
    return render_template('order.html')

@app.route('/chatbot.html')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/history.html')
def history_page():
    return render_template('history.html')


if __name__ == '__main__':
    app.run(debug=True)
