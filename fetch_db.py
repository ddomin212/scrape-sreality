import psycopg2

def fetch_sreality():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="secret",
        port=5432
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a SELECT * statement
    cur.execute("SELECT * FROM sreality_table")

    # Fetch all the results and store them in a list
    results = cur.fetchall()

    # Close the cursor and database connection
    cur.close()
    conn.close()

    # Print the list of results
    return results
