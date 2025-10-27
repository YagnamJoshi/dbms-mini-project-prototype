from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yagnamjoshi",  # change this
        database="mini_project"
    )

# --- Homepage ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Clubs List ---
@app.route('/clubs')
def clubs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('getClubInfo')

    clubs = []
    for result in cursor.stored_results():
        clubs = result.fetchall()

    cursor.close()
    conn.close()
    return render_template('clubs.html', clubs=clubs)

# --- Club Detail ---
@app.route('/club/<club_name>')
def club_detail(club_name):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # club info
    cur.execute("""
        SELECT c.clubID, c.clubName, c.clubSecretary, d.departmentName, f.facultyName AS facultyAdvisor
        FROM club c
        JOIN department d ON c.departmentID = d.departmentID
        JOIN faculty f ON c.facultyID = f.facultyID
        WHERE c.clubName = %s
    """, (club_name,))
    club = cur.fetchone()

    if not club:
        cur.close()
        conn.close()
        return f"<h2>No club found with name: {club_name}</h2>"

    # members
    cur.execute("""
        SELECT s.studentName
        FROM student s
        JOIN student_club_details scd ON s.PRN = scd.PRN
        WHERE scd.clubID = %s
        ORDER BY s.studentName;
    """, (club['clubID'],))
    members = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('club_detail.html', club=club, members=members)

if __name__ == "__main__":
    app.run(debug=True)
