import mysql.connector
import re
import pandas as pd
import numpy as np
from sklearn import linear_model
import pickle
filename = "finalized_model.sav"
loaded_model = pickle.load(open(filename, 'rb'))

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="hackathon"
)
mycursor=db.cursor()


#mycursor.execute("ALTER TABLE user ADD COLUMN rating ENUM('1','2','3','4') NOT NULL")
#mycursor.execute("""CREATE TABLE market_current 
#(order_id int PRIMARY KEY AUTO_INCREMENT NOT NULL, 
#user_id int NOT NULL,
#user_name varchar(50),
#crop VARCHAR(50) NOT NULL, 
#quantity int NOT NULL, 
#price int NOT NULL
#)""")

#mycursor.execute("INSERT INTO market_current(user_id,user_name) VALUES (%s,%s)",(1,user1))
#mycursor.execute("INSERT INTO user (username,password) VALUES (%s,%s)",("user1","12345"))
def register(username,password):
    mycursor.execute("INSERT INTO user(username,password) VALUES (%s,%s)",(username,password))

def sell(crop,quantity,price,username):
    try:
        mycursor.execute("SELECT id FROM user WHERE username=%s",(username,))
        for i in mycursor:
            id=i[0]
    except:
        return "username not found"
    mycursor.execute("INSERT INTO market_current(user_id,user_name,crop,quantity,price) VALUES (%s,%s,%s,%s,%s)",(id,username,crop,quantity,price))


def show_user():
    mycursor.execute("SELECT * FROM user")
    for x in mycursor:
        print(x)

def show_marketcurrent():
    mycursor.execute("SELECT * FROM market_current")
    for x in mycursor:
        print(x)
lst=[]
def show_pre_order_market():
    mycursor.execute("SELECT * FROM pre_order_market")
    for x in mycursor:
        lst.append(x)
        print(x)


#mycursor.execute("""CREATE TABLE pre_order_market(pre_order_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,
#crop VARCHAR(50) NOT NULL, 
#predicted_quantity int NOT NULL, 
#est_harvest_date VARCHAR(50) NOT NULL,
#price int NOT NULL
#)""")


def pre_sell(username,crop,price,harvestdate,area,soil_type):
    soil=[]
    if soil_type=="chalky":
        soil=[1,0,0,0,0,0,0]
    if soil_type=='clay':
        soil=[0,1,0,0,0,0,0]
    if soil_type=='loamy':
        soil=[0,0,1,0,0,0,0]
    if soil_type=='peaty':
        soil=[0,0,0,1,0,0,0]
    if soil_type=='sandy':
        soil=[0,0,0,0,1,0,0]
    if soil_type=='silt':
        soil=[0,0,0,0,0,1,0]
    if soil_type=='silty':
        soil=[0,0,0,0,0,0,1]
    temperature=24.647
    Precipitaion=17.4454
    Humidity=40
    x=[area,temperature,Precipitaion,Humidity]+soil
    pattern=r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})'
    if not (re.search(pattern,harvestdate)):
        print('pls insert a date')
        return 'please insert a date'
    try:
        mycursor.execute("SELECT id FROM user WHERE username=%s",(username,))
        for i in mycursor:
            id=i[0]
    except:
        print("username not found")
        return "username not found"
    predicted_quantity=loaded_model.predict([x])
    predicted_quantity=predicted_quantity[0]
    mycursor.execute("INSERT INTO pre_order_market(crop,predicted_quantity,est_harvest_date,price) VALUES (%s,%s,%s,%s)",(crop,predicted_quantity,harvestdate,price))

#
register('user1','12345')
pre_sell('user1','wheat',50,'02/02/2022',10300,'clay')
show_pre_order_market()
print(lst)
print("done")
   