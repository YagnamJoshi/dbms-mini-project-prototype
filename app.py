from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# -------------------------------
# 🔌 DATABASE CONNECTION FUNCTION
# -------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",              # change if different
        password="yagnamjoshi", # change to your MySQL password
        database="mini_project"     # your existing database
    )

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------------
# 📋 CLUBS PAGE
# -------------------------------
@app.route('/clubs')
def clubs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('get_all_clubs')
    result = list(cursor.stored_results())[0]
    clubs = result.fetchall()
    cursor.close()
    conn.close()
    return render_template('clubs.html', clubs=clubs)


# -------------------------------
# 🔍 CLUB DETAIL PAGE
# -------------------------------
@app.route('/club/<club_name>')
def club_detail(club_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('get_club_details', [club_name])
    result = list(cursor.stored_results())[0]
    details = result.fetchall()
    cursor.close()
    conn.close()
    return render_template('club_detail.html', details=details, club_name=club_name)


# -------------------------------
# 🎉 EVENTS PAGE
# -------------------------------
@app.route('/events')
def events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('get_all_events')
    result = list(cursor.stored_results())[0]
    events = result.fetchall()
    cursor.close()
    conn.close()
    return render_template('events.html', events=events)


# -------------------------------
# 🔎 SEARCH FUNCTIONALITY
# -------------------------------
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM club WHERE clubName LIKE %s", (f"%{query}%",))
    clubs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clubs.html', clubs=clubs, search_query=query)


# -------------------------------
# 🚀 RUN SERVER
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
