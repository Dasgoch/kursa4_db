from app import app
import view
import psycopg2

con = psycopg2.connect(
    database="d80d6ankv1spjo",
    user="zqpibjvpnhqcvv",
    password="03db86573ea167252b57198f00a688d34f6869c5012ecd6865208a57086d3cc0",
    host="ec2-54-247-177-254.eu-west-1.compute.amazonaws.com",
    port="5432"
)
cur = con.cursor()


if __name__ == '__main__':
    app.run()
