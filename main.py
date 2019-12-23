from app import app
import view
import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1234",
    host="127.0.0.1",
    port="5432"
)
cur = con.cursor()


if __name__ == '__main__':
    app.run()
