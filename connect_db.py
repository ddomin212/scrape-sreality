import psycopg2

def connect_PSQL():
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="secret",
        port=5432
    )
    # $ docker run --name postgres-container -e POSTGRES_PASSWORD=secret -d -p 5432:5432 postgres
    # $ docker exec -it postgres-container psql -U postgres
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS sreality_table (id SERIAL PRIMARY KEY, name VARCHAR(50), img1 VARCHAR(150), img2 VARCHAR(150), img3 VARCHAR(150))")
    conn.commit()
    cur.close()
    conn.close()