# coding=utf-8 1

from flask import render_template, flash, redirect,  make_response, session, url_for, request, g, Markup
from flask_login import login_required, logout_user, current_user, login_user, logout_user
from app import app, db
from app import login_manager
from app.forms import QueryForm, SignupForm, LoginForm
from app.models import Student
import mysql.connector
import psycopg
from mysql.connector import Error


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Student.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if request.method == 'POST':
        user = Student.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/createdb')
def createdb():
    db.create_all()
    return make_response("db created successfully created!")

@app.route('/sregister', methods=['GET','POST'])
def sregister():
    form=SignupForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        print(form.email.data)
        existing_user=Student.query.filter_by(email=form.email.data).first()
        print(existing_user)
        if existing_user is None:
            new_user= Student(
                email=form.email.data, 
                fname=form.fname.data, 
                lname=form.lname.data,
                classcode=form.classcode.data,
            )
            print(new_user)
            new_user.set_password(form.password.data) 
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        flash('A user already exists with that email address.')
    else:
        flash('Not validated.')

    return render_template('sregister.html', form=form)


@app.route('/queryw', methods=['GET','POST'])
@login_required
def queryw():
    form=QueryForm()
    if request.method == 'POST':
    #if form.validate_on_submit():
        sqlin=request.form.get('querybody')
        session['sqltorun']=sqlin
        print(sqlin)
        print(session['sqltorun'])
        import urllib
        from_data={'sql':sqlin}
        import json
        params=json.dumps(from_data)
        #params = urllib.urlencode(form_data)
        print(params)
        #return render_template('display.html',headers=headers,results=results)
        return redirect(url_for('displayw'))
    
    return render_template('querywindow.html', form=form)


@app.route('/question', methods=['GET','POST'])
def question():
    form=QueryForm()
    headers=[]
    results=[]
    QText=""
    try:
        connection=psycopg.connect("dbname=exercises user=ist host=localhost port=5432 password=ist")
        cursor = connection.cursor()
        sql = "select * from question where id=1001;"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        QText=result[2]
        QAnswer=result[3]
        print("Test:"+QText)
        print("Answer:"+QAnswer)
        #get the correct answer
        cursor.close()
        connection.close()
        try:
            connection=psycopg.connect("dbname=exercises user=ist host=localhost port=5432 password=ist")
            cursor = connection.cursor()
            cursor.execute(QAnswer)
            #correct answer becomes a session variable
            session['sqlanswer']=QAnswer
            print(session['sqlanswer'])
            for x in cursor.description:
                print(x)
                headers = [i[0] for i in cursor.description]
                print(headers)
            results = cursor.fetchall()
            for x in results:
                print(x)
            cursor.close()
            connection.close()
        except:
            print("error")
            print(psycopg.OperationalError)
    except:
        print("error")
        print(psycopg.OperationalError)

    if request.method == 'POST':
        #if form.validate_on_submit():
        sqlin=request.form.get('querybody')
        session['sqltorun']=sqlin
        print(sqlin)
        print(session['sqltorun'])

        #import urllib
        #from_data={'sql':sqlin}
        #import json
        #params=json.dumps(from_data)
        #params = urllib.urlencode(form_data)
        #print(params)
        #return render_template('display.html',headers=headers,results=results)
        return redirect(url_for('displayquestionresult'))

    return render_template('question.html', headers=headers,results=results, form=form, qtext=QText)


@app.route('/displayw')
def displayw():
    #req_data=request.get_json()
    #sql=req_data['sqlin']
    #sql=request.form.get('querybody')
    headers=[]
    results=[]
    sql=session['sqltorun']
    #print(sql)
    session.pop('sqltorun', None)
    #sql="select * from shipment;"
    try:
        connection=psycopg.connect("dbname=exercises user=ist host=localhost port=5432 password=ist")
        #connection=psycopg.connect("postgresql://ist:ist@127.0.0.1:5432/exercises")
        print(connection)
        print(sql)
        cursor=connection.cursor()
        cursor.execute(sql)
        headers = [desc[0] for desc in cursor.description]
        results=cursor.fetchall()
        for x in results:
                print(x)
        cursor.close()
        connection.close()
    except:
        print("error")
        print(psycopg.OperationalError)
    
    return render_template('displayw.html',sql=sql, headers=headers,results=results)


@app.route('/displayw_mysql')
def displayw_mysql():
    #req_data = request.get_json()
    #sql = req_data['sqlin']
    #sql=request.form.get('querybody')
    sql=session['sqltorun']
    print(sql)
    session.pop('sqltorun', None)
    try:
        connection = mysql.connector.connect(host='istdata.bk.psu.edu', database='auk3', user='auk3', password='auk3')   
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            #cursor.execute("select database();")
            #record = cursor.fetchone()
            #print("You're connected to database: ", record)
            #sql = "SELECT * FROM shipment"
            cursor = connection.cursor()
            cursor.execute(sql)
            for x in cursor.description:
                print(x)
            headers = [i[0] for i in cursor.description]
            print(headers)
            results = cursor.fetchall()
            for x in results:
                print(x)

    except Error as e:
            print("Error while connecting to MySQL", e)

    return render_template('displayw.html',sql=sql, headers=headers,results=results)


@app.route('/displayquestionresult')
def displayquestionresult():
    #req_data = request.get_json()
    #sql = req_data['sqlin']
    #sql=request.form.get('querybody')
    sql=session['sqltorun']
    print(sql)
    session.pop('sqltorun', None)
    
    #correct answer becomes a session variable
    sqlanswer=session['sqlanswer']
    session.pop('sqlanswer', None)
    headers=[]
    print(sql)
    
    try:
        connection=psycopg.connect("dbname=exercises user=ist host=localhost port=5432 password=ist")
        cursor = connection.cursor()
        cursor.execute(sql)
        for x in cursor.description:
            print(x)
        headers = [i[0] for i in cursor.description]
        print(headers)
        results = cursor.fetchall()
        results_n=cursor.rowcount
        for x in results:
            print(x)
        cursor.close()    
        connection.close()
    except:
        print("error")
        print(psycopg.OperationalError)

    try:
        connection=psycopg.connect("dbname=exercises user=ist host=localhost port=5432 password=ist")
        cursor = connection.cursor()
        cursor.execute(sqlanswer)
        for x in cursor.description:
            print(x)
        cheaders = [i[0] for i in cursor.description]
        print(headers)
        cresults = cursor.fetchall()
        cresults_n=cursor.rowcount    
        if cresults_n != results_n:
            message='Try Again!'
        else:
            message='Well Done! Move to the next level'  
    
        for x in cresults:
            print(x)
        cursor.close()    
        connection.close()
    except:
        print("error")
        print(psycopg.OperationalError)  

    return render_template('displayquestionresult.html',sql=sql, headers=headers,results=results, cheaders=cheaders,cresults=cresults, message=message)


