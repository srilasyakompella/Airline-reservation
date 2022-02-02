from flask import Flask, render_template, request
import requests
import random
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="nikhilnikhil",auth_plugin='mysql_native_password', database='testdb')


app = Flask(__name__,template_folder='templates')

if(mydb):
    print("Connected to ")
    print(mydb)
else:
    print('Nah')
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM flight  ORDER BY CHARGES")
myresult = mycursor.fetchall()
pid=0
sno=0
l=[]
for x in myresult:
    l.append(x)


  
@app.route('/flights',methods=['POST'])
def flights():
    fromCity= request.form['fromCity']
    toCity= request.form['toCity']
    departureDate= request.form['departureDate']
    firstName=request.form['fname']
    lastName=request.form['lname']
    email=request.form['email']
    phoneNo=request.form['phno']
    age=request.form['age']
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
    li=[x for x in range(1,700)]
    passengerId=random.choice(li)
    global pid 
    pid=passengerId
    print('Passenger id in flights is :',pid)
    mycursor.execute('insert into passengerDetails values(%s,%s,%s,%s,%s)',(pid,name,age,email,phoneNo) )
    mydb.commit()
    # mycursor.execute("SELECT * FROM passengerDetails where passengerId=passId ")
    # result = mycursor.fetchall()
    # x=[]
    # for i in result:
    #     x.append(i)
    # print(x)
    for i in range(1,passengers):
        passengerId=random.choice(li)
        fn=(request.form['fname'+str(i)])
        ln=(request.form['lname'+str(i)])
        e=(request.form['email'+str(i)])
        p=(request.form['phno'+str(i)])
        a=(request.form['age'+str(i)])
        s=fn+ln
        mycursor.execute('insert into passengerDetails values(%s,%s,%s,%s,%s)',(passengerId,s,a,e,p))
        mydb.commit()
       
   
    return render_template('home.html',l=l,fromCity=fromCity,toCity=toCity)
@app.route('/Page4',methods=['POST'])
def Page4():
    id= request.form['abc']
    global sno
    sno= id
    # print(id)
    return render_template('Page4.html')
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
        return render_template('Page5.html')
    else:
        return render_template('Page4.html')
@app.route('/Page2',methods=['POST','GET'])
def Page2():
    if request.method=='POST':
        name= request.form['name']
        password= request.form['password']
        print(name)
        print(password)
        mycursor.execute('insert into test values(%s,%s)',(name,password) )
        mydb.commit()
        return render_template('Page2.html')
    else:
        return render_template('Page1.html')

@app.route('/',methods=['GET'])
def home():
    return render_template('Page1.html')



if __name__=='__main__':
    app.run(debug=True)