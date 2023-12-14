from flask import Flask, render_template, request, jsonify
import mysql.connector
import os 

app = Flask(__name__)

def create_connection():
    conn = None
    try:
        db_password = os.getenv('MYSQL_PASSWORD')

        conn = mysql.connector.connect(user='root', password=db_password, host='localhost')
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS studentdb")

        conn = mysql.connector.connect(user='root', password=db_password, host='localhost', database='studentdb')
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE()")
        info = cursor.fetchone()
        print("Connection established to: ", info)

    except Exception as e:
        print(e)
    return conn

def create_student_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS student (id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), address VARCHAR(100))")
        print("Table 'student' created successfully")
    except Exception as e:
        print(e)

def insert_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0]
    if count == 0: 
        data = [
            (1, 'Maria', 'DelMar', '123 Main St'),
            (2, 'Alice', 'Smith', '456 Elm St'),
            (3, 'Chris', 'Thompson', '789 Oak St'),
            (4, 'Emma', 'Pearson', '101 Pine St'),
            (5, 'Nathalia', 'Gonzalez', '202 Cedar St')
        ]
        cursor.executemany("INSERT INTO student(id, first_name, last_name, address) VALUES(%s, %s, %s, %s)", data)
        conn.commit()

def get_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM student''')
    rs = cursor.fetchall()
    return rs

def add_student(conn, data):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO student(id, first_name, last_name, address) VALUES(%s, %s, %s, %s)", data)
        conn.commit()
        print("Student added successfully.")
    except Exception as e:
        print(e)

def remove_student(conn, student_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE id = %s", (student_id,))
        conn.commit()
        print("Student removed successfully.")
    except Exception as e:
        print(e)

connection = create_connection()
create_student_table(connection)

@app.route('/')
def show_names():
    student_data = get_data_from_db(connection)
    return render_template('index.html', students=student_data)

@app.route('/add_student', methods=['POST'])
def add_student_route():
    new_student = (
        int(request.form['id']),
        request.form['firstName'],
        request.form['lastName'],
        request.form['address']
    )
    add_student(connection, new_student)
    return jsonify({"message": "Student added successfully"})

@app.route('/remove_student', methods=['POST'])
def remove_student_route():
    remove_id = int(request.form['removeId'])
    remove_student(connection, remove_id)
    return jsonify({"message": "Student removed successfully"})

if __name__ == '__main__':
    app.run(debug=True)

