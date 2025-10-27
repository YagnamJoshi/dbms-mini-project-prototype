import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yagnamjoshi",
    database="mini_project"
)

cursor = conn.cursor()

# Call stored procedure
cursor.callproc('get_all_clubs')
result = list(cursor.stored_results())[0]
rows = result.fetchall()

# Loop through all result sets
print("Club Table Data:")
print("--------------------")
for club in rows:
    print(f"ClubID: {club[0]} | ClubName: {club[1]} | Secretary: {club[2]} | FacultyID: {club[3]} | DepartmentID: {club[4]}")

cursor.close()
conn.close()