from flask import Flask, render_template, request
import requests
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
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

l=[]
for x in myresult:
    l.append(x)

@app.route('/Page4',methods=['POST'])
def Page4():
    id= request.form['abc']
    print(id)
    return render_template('Page4.html')
  
@app.route('/flights',methods=['POST'])
def flights():
    fromCity= request.form['fromCity']
    toCity= request.form['toCity']
    departureDate= request.form['departureDate']
    print(fromCity)
    print(toCity)
    print(departureDate)
    return render_template('home.html',l=l,fromCity=fromCity,toCity=toCity)

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