from flask import Flask, render_template, request
from flask_mail import Mail
from flask_mail import Mail, Message
import requests
import random
import mysql.connector
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email import encoders
import smtplib
import os
import json
mydb=mysql.connector.connect(host="localhost",user="root",passwd="nikhilnikhil",auth_plugin='mysql_native_password', database='testdb')


app = Flask(__name__,template_folder='templates')
app.config['MAIL_SERVER']='http://smtp.gmail.com/'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'airline project'
app.config['MAIL_PASSWORD'] = 'airline-proj@1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM flight  ORDER BY CHARGES")
myresult = mycursor.fetchall()
pid=0
sno=0
bid=0
email=""
passengers=0
departureDate=0
l=[]
for x in myresult:
    l.append(x)
@app.route('/flights',methods=['POST'])
def flights():
    fromCity= request.form['fromCity']
    toCity= request.form['toCity']
    global departureDate
    departureDate= request.form['departureDate']
    firstName=request.form['fname']
    lastName=request.form['lname']
    global email
    email=request.form['email']
    phoneNo=request.form['phno']
    age=request.form['age']
    global passengers
    passengers=int(request.form['passengers'])
    name=firstName+lastName
    print(fromCity)
    print(toCity)
    print(departureDate)
    print(passengers)
    print(firstName)
    print(lastName)
    print(email)
    print(phoneNo)
    print(age)
    li=[x for x in range(700,99999)]
    passengerId=random.choice(li)
    bi=[x for x in range(1,99999)]
    global bid
    bid=random.choice(bi)
    global pid 
    pid=passengerId
    print('Passenger id in flights is :',pid)
    mycursor.execute('insert into passengerDetails values(%s,%s,%s,%s,%s,%s)',(pid,name,age,email,phoneNo,bid) )
    mydb.commit()
    for i in range(1,passengers):
        passengerId=random.choice(li)
        fn=(request.form['fname'+str(i)])
        ln=(request.form['lname'+str(i)])
        e=(request.form['email'+str(i)])
        p=(request.form['phno'+str(i)])
        a=(request.form['age'+str(i)])
        s=fn+ln
        mycursor.execute('insert into passengerDetails values(%s,%s,%s,%s,%s,%s)',(passengerId,s,a,e,p,bid))
        mydb.commit()
    return render_template('home.html',l=l,fromCity=fromCity,toCity=toCity)
@app.route('/Page4',methods=['POST'])
def Page4():
    id= request.form['abc']
    global sno
    sno= id
    mycursor.execute('SELECT * FROM flight where flightId=%s',(sno,))
    y = mycursor.fetchall()
    totalFare=y[0][-1]
    print(passengers)
    return render_template('Page4.html',totalFare=totalFare*passengers)
@app.route('/Page5',methods=['POST','GET'])
def Page5():
    if request.method=='POST':
        cardNumber=request.form['cardNumber']
        cardOwnerName=request.form['cardOwnerName']
        print(cardNumber)
        print(cardOwnerName)
        li=[x for x in range(1,9000)]
        paymentId=random.choice(li)
        print('Passenger id in page5 is :',pid)
        print(pid)
        mycursor.execute('insert into payment values(%s,%s,%s,%s,%s)',(pid,sno,cardOwnerName,cardNumber,paymentId) )
        mydb.commit()
        mycursor.execute('SELECT * FROM flight where flightId=%s',(sno,))
        x = mycursor.fetchall()
        indcharge=x[0][-1]
        mycursor.execute('SELECT * FROM passengerDetails where bookingId=%s',(bid,))
        y = mycursor.fetchall()
        data=[]
        for i in range(len(y)):
            data.append(y[i][1])
        # server = smtplib.SMTP('smtp.gmail.com' , 587)
        # server.starttls()
        # server.login('airlineproj@gmail.com' , 'airline-proj@1')
        # server.sendmail('airlineproj@gmail.com' , 'psaipreeti@gmail.com' , 'mail from me')
        # print('mail sent')
        return render_template('Page5.html',flightDetails=x,passengersNames=data,totalCharges=passengers*indcharge,passengers=passengers,departureDate=departureDate)
    else:
        return render_template('Page4.html')
@app.route('/Page6',methods=['POST','GET'])
def Page6():
    if request.method=='POST':
        sender = 'airlineproj@gmail.com'
        receiver = email
        subject = "Ticket booked successfully"
        message = f"""From: From <{sender}>
        To: To <{receiver}>
        MIME-Version: 1.0
        Content-type: text/html
        Subject: {subject}

        Your ticket had been booked successfully!!!

        """
        server = smtplib.SMTP('smtp.gmail.com' , 587)

        server.starttls()
        server.login(sender , 'airline-proj@1')

        server.sendmail(sender , receiver , message)
        return render_template('Page6.html')
        
@app.route('/Page2',methods=['POST','GET'])
def Page2():
    name=""
    password=""
    if request.method=='POST':
        name= request.form['name']
        password= request.form['password']
        print(name)
        print(password)
        mycursor.execute("SELECT * FROM userDetails")
        det=mycursor.fetchall();
        c=0
        for i in range(len(det)):
            if(det[i][0]==name and det[i][1]==password):
                c=1
                s=0
                return render_template('Page2.html')
            elif(det[i][0]==name and det[i][1]!=password):
                c=1
                s=1
                print(s)
                return render_template('Page1.html',s=s) 
        if c==0:
            return render_template('Page1.html',c=c)
    else:
        return render_template('Page1.html',s=0)
    
@app.route('/Signup',methods=['POST'])
def Signup():
    if request.method=='POST':
        return render_template('signup.html')
@app.route('/Signin',methods=['POST'])
def Signin():
    name=request.form['name']
    pwd=request.form['password']
    print(name)
    print(pwd)
    mycursor.execute("INSERT INTO userDetails VALUES(%s,%s)",(name,pwd))
    mydb.commit()
    if request.method=='POST':
        return render_template('Page1.html')

@app.route('/',methods=['GET'])
def home():
    return render_template('Page1.html')



if __name__=='__main__':
    app.run(debug=True)