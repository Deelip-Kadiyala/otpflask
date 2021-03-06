from flask import Flask, render_template , request , session
from flask_mysqldb import MySQL
from twilio.rest import Client
import MySQLdb
import random
import smtplib

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'deelip'
app.config['MYSQL_PASSWORD'] = 'apple'
app.config['MYSQL_DB'] = 'testing1'

mysql = MySQL(app)
@app.route("/", methods=['GET','POST'])
def login():
    return render_template("./frontend_test.html")

@app.route("/testing", methods=['GET','POST'])
def getemail():
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("select email from userstest where fname='"+firstName+"'")
        for email in cur:
            print(email[0])
        mysql.connection.commit()
        cur.close()
        return "sucess"