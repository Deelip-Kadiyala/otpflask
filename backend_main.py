from flask import Flask, render_template , request , session
from flask_mysqldb import MySQL
# from twilio.rest import Client
import MySQLdb
import random
import smtplib

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'deelip'
app.config['MYSQL_PASSWORD'] = 'apple'
app.config['MYSQL_DB'] = 'testing1'

mysql = MySQL(app)

global_otp=000000
global_email ="hello"

s = smtplib.SMTP('smtp.gmail.com', 587)


@app.route("/", methods=['GET','POST'])
def loginform():
    return render_template('./index.html')

@app.route("/register", methods=['GET','POST'])
def signupform():
    return render_template('./Registration.html')

@app.route("/saving_details", methods=['GET','POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        email = details['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO userstest(fname, lname, email) VALUES (%s, %s, %s)", (firstName, lastName, email))
        mysql.connection.commit()
        cur.close()
        return 'success'


def generateotp():
    return random.randrange(100000,999999)

def getOTPapi(email):
    global global_otp

    global_otp=generateotp()

    s.starttls() 
    # Authentication 
    s.login("techwithdnp@gmail.com", "qyzhtuojpnpcympd") 
    # message to be sent 
    message = "Here is your OTP "+str(global_otp)
    # sending the mail 
    s.sendmail("techwithdnp@gmail.com", email, message) 
  
    # terminating the session 
    s.quit()
    return global_otp

@app.route("/enterOTP", methods=['GET','POST'])
def getemail():
    global global_email
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("select email from userstest where fname='"+firstName+"'")
        for email in cur:
            global_email=email[0]
        mysql.connection.commit()
        cur.close()
        global global_otp
        global_otp=getOTPapi(global_email)
        enterotp_frontend='<html><title>OTP</title><body><form method="POST" action="/verifyOTP" ><center><h1>OTP Sent to your Registered Email ID:'+global_email+'</h1><h2>Please Enter OTP </h2>OTP <input type="text" name="otp"><input type = "submit" name="Verify"></center></form></body></html>'

    return enterotp_frontend


@app.route("/verifyOTP",methods=['POST'])
def verifyotp():
    global global_otp
    otp=request.form['otp']

    if str(global_otp) == str(otp):
        return 'You are Authorized!'
    else:
        return 'You are not Authorized!, Sorry!'


if __name__ == '__main__':
    app.run()