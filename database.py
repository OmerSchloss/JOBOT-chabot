
# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database_name'
}


def save_answer(question, answer):
    print(question)
    print(answer)
    # Establish database connection
    # conn = mysql.connector.connect(**db_config)
    # cursor = conn.cursor()

    # Insert user's answer into the database
    # insert_query = "INSERT INTO user_answers (question, answer) VALUES (%s, %s)"
    # cursor.execute(insert_query, (question, answer))

    # Commit the changes and close the connection
    # conn.commit()
    # cursor.close()
    # conn.close()
