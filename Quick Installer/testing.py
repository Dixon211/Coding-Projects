import sqlite3

conn = sqlite3.connect('programs_to_install.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT statement
cursor.execute("SELECT * FROM software_values")

# Fetch all the rows returned by the SELECT statement
rows = cursor.fetchall()

# Iterate over the rows and process the data
for row in rows:
    # Access the data in each row using indexing or column names
    column1_value = row[0]

    # Process the data as needed
    print(column1_value)

# Close the cursor and connection
cursor.close()
conn.close()