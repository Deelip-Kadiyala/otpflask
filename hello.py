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
app.secret_key = 'otp'
global_otp=000000

s = smtplib.SMTP('smtp.gmail.com', 587)


@app.route("/testing", methods=['GET','POST'])
# @app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO userstest(fname, lname) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('./frontend_email.html')
@app.route("/", methods=['GET','POST'])
def getOTP():
    return render_template('./frontend_test.html')

def generateotp():
    return random.randrange(100000,999999)

def getOTPapi(email):
    global global_otp
    # account_sid='AC6ec85c67a0dca260538d67dc25a25734'
    # auth_token='6b85661608ad083a48ec95c125c06ecb'
    # client= Client(account_sid,auth_token)
    global_otp=generateotp()
    # session['response'] = str(otp)
    # body="This is your Testing OTP from seema pig : "+str(otp)
    # message=client.messages.create(from_='+18053016693',body=body,to=phno)
    # if message.sid:
    #     return True
    # else:
    #     return False
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

@app.route("/enterOTPformemail", methods=['GET','POST'])
def enterotp():
    global global_otp
    # phno=request.form["phno"]
    # val=getOTPapi(phno)
    email=request.form["email"]
    global_otp=getOTPapi(email)
    return render_template('./enterotp_frontend.html')

@app.route("/verifyOTP",methods=['POST'])
def verifyotp():
    global global_otp
    otp=request.form['otp']
    # if 'response' in session:
    #     s = session['response']
    #     session.pop('response',None)
    #     if s == otp:
    #         return 'You are Authorized, Thank you'
    #     else:
    #         return 'You are not Authorized, Sorry!'
    # return str(global_otp)+'___'+str(otp)
    if str(global_otp) == str(otp):
        return 'You are Authorized!'
    else:
        return 'You are not Authorized!, Sorry!'


if __name__ == '__main__':
    app.run()