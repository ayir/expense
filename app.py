from flask import Flask, redirect, render_template, request, url_for, flash, session
from db import db
from pymsgbox import *

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_db')
def create_db():
    db.create_db()
    return "created"


@app.route('/log-in', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        value = db.authenticate(
            request.form['username'],
            request.form['password'])
        if (value == 1):
            print ("Succesful")
            session['name'] = request.form['username']
            user_data = session['name']
            print (user_data)
            data = db.filter_user_data(user_data)
            print (type(data), data, len(data))
            data_user_get = db.filter_user_chart(user_data)
            graph_data = []
            for elem in data_user_get:
                cat = elem[0]
                exp = elem[1]
                li = [cat, int(exp)]
                graph_data.append(li)
            graph_data.insert(0, ['Category', 'Expenses'])
            print ("Graph data ", graph_data)
            return render_template(
                'index.html',
                error=error,
                data=data,
                data_chart=graph_data)
        else:
            alert(text='INVALID INPUT', title='ERROR', button='OK')
            return render_template('login.html', error=error, session=session)
    return render_template('login.html')


@app.route('/reg?is%2')
def registration():
    return render_template('registration.html')


@app.route("/registform", methods=['POST'])
def register():
    data = db.user_alreadyexits(request.form['field2'],
                                request.form['field1'],
                                request.form['field3'])
                                
                               
    if (data == 1):
        alert(text='USER ALREADY EXISTS/INVALID INPUT', title='ERROR', button='OK')
        return redirect(url_for('registration'))
    print (data)
    alert(text='REGISTRATION SUCCESSFUL', title='SUCCESSFUL', button='OK')
    return redirect(url_for('registration'))


@app.route('/login')
def index():
    error = None
    user_data = session['name']
    print (user_data)
    data = db.filter_user_data(user_data)
    print (type(data), data, len(data))
    data_user_get = db.filter_user_chart(user_data)
    graph_data = []
    for elem in data_user_get:
        cat = elem[0]
        exp = elem[1]
        li = [cat, int(exp)]
        graph_data.append(li)
    graph_data.insert(0, ['Category', 'Expenses'])
    print ("Graph data ", graph_data)
    return render_template(
        'index.html',
        error=error,
        data=data,
        data_chart=graph_data,
        session=session)


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/clearsession')
def clearsession():
    session.clear()
    return redirect(url_for('logina'))



@app.route('/log-in')
def logina():
    return render_template('login.html')


@app.route('/add')
def add():
    return render_template('add_catagories.html')


@app.route("/category", methods=['POST'])
def category():
    error = None
    data_category = db.category_alreadyexits(session['name'],
                                             request.form['field7'],
                                             request.form['field8'],
                                             request.form['field9'])
    if (data_category == 1):
        alert(text='CATEGORY ALREADY EXISTS/INPUT MISMATCH', title='ERROR', button='OK')
    else:
        flash(data_category)
        user_data = session['name']
        print (user_data)
        data = db.filter_user_data(user_data)
        print (type(data), data, len(data))
        data_user_get = db.filter_user_chart(user_data)
        graph_data = []
        for elem in data_user_get:
            cat = elem[0]
            exp = elem[1]
            li = [cat, int(exp)]
            graph_data.append(li)
        graph_data.insert(0, ['Category', 'Expenses'])
        print ("Graph data ", graph_data)
        return render_template(
            'index.html',
            error=error,
            data=data,
            data_chart=graph_data)
    flash('REQUEST PERFORMED!')
    return redirect('add')




if __name__ == '__main__':
    app.run()
