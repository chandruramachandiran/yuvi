from flask import Flask,render_template,request,redirect,url_for
from flask_mail import Mail,Message
from pymongo import *
from datetime import datetime


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pondicherryfashionmodels@gmail.com'
app.config['MAIL_PASSWORD'] = 'dhoni110299'

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/reg')
def index():
    return render_template('reg.html')
@app.route("/registration",methods=['POST'])
def register():
    name=request.form['name']
    dob=request.form['birthday']
    gender=request.form['gender']
    email=request.form['email']
    mobile=request.form['phone']
    con = MongoClient("mongodb+srv://yuvi:112@cluster0.ivajb.mongodb.net/register?retryWrites=true&w=majority")
    db = con['register']
    col = db['date check']
    for m in col.find():
        now = datetime.now()
        end = datetime(m['year'], m['month'], m['date'], m['hour'], m['min'])
        col = db['reg']
        if (now < end):
            if (name!='')and(dob!='')and(gender!='')and(email!='')and(mobile!=''):
                for i in col.find({"gmail":email}):
                    return render_template('reg.html',msg='This gmail is alread exist')
                else:
                    l = 0
                    for j in col.find():
                        l=j['entry_no']
                    col.insert_one({'name':name,'bday':dob,'sex':gender,'gmail':email,'mobile':mobile,'entry_no':l+1})
                    msg = Message('Welcome to Pondicherry Fashion Models', sender='pondicherryfashionmodels@gmail.com', recipients=[email])
                    a = str(l + 1)
                    msg.body = 'Hai'" "+name+', your Entry number is '+a+", Your registration is done."
                    mail.send(msg)
                    return redirect(url_for('tabel'))
            else:
                return render_template('reg.html',msg='Fill the entire form')
        else:
            return render_template('reg.html',msg="Registeration is closed")
@app.route('/tabel')
def tabel():
    con = MongoClient("mongodb+srv://yuvi:112@cluster0.ivajb.mongodb.net/register?retryWrites=true&w=majority")
    db = con['register']
    col = db['reg']
    res=[]
    for k in col.find():
        res.append(k)
    return render_template('table2.html',data=res)
@app.route('/search',methods=['POST'])
def index1():
    search=request.form['search']
    con = MongoClient("mongodb+srv://yuvi:112@cluster0.ivajb.mongodb.net/register?retryWrites=true&w=majority")
    db = con['register']
    col = db['reg']
    r = []
    for q in col.find({'name':search}):
        r.append(q)
        return render_template('search.html',res=r)
    else:
        return render_template("index.html", msg='Enter the name as same as you entered in form or Name is not found')
app.run(debug=True)