from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '******'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'sparks'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return render_template('spark1.html')

@app.route('/second',methods=['GET'])
def hello():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        query = "Select *from customers"
        cur.execute(query)
        all_cust=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('cust.html',all_cust=all_cust) #in red will be used in cust.html

@app.route('/third',methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        sname = userDetails['s_name']  # s_name in html file
        sacct = userDetails['s_acct']
        rname = userDetails['r_name']
        racct = userDetails['r_acct']
        amount = userDetails['amt']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO transfers(SendersName,ReceiversName,S_Account_no,R_Account_no,Amount) VALUES(%s, %s,%s, %s,%s)",
        (sname, rname, sacct, racct, amount))
        cur.execute(f"UPDATE customers SET Current_balance=Current_balance+{amount} WHERE Account_no={racct}")
        cur.execute(f"UPDATE customers SET Current_balance=Current_balance-{amount} WHERE Account_no={sacct}")
        mysql.connection.commit()
        cur.close()
        return render_template('transfer.html')
    return render_template('transfer.html')

@app.route('/fourth',methods=['GET'])
def hist():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        query = "Select *from transfers"
        cur.execute(query)
        transfers=cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('history.html',transfers=transfers)

app.run(debug=True)




