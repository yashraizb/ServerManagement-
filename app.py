from flask import Flask,render_template,redirect, url_for,request,session,app
from flask_mysqldb import MySQL
from datetime import timedelta
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kahtras'
app.config['MYSQL_PASSWORD'] = 'kahtras'
app.config['MYSQL_DB'] = 'serverpanel'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=360)


def dbsearch(email):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT Email,Password,Username FROM UserInfo WHERE Email = "{email}"')
    rv = cur.fetchall()
    return rv

def dbservers():
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT Servername,ServerIp FROM Userservers')
    rv = cur.fetchall()
    return rv




@app.route('/')
def route_index():
        if 'username' in session:
            username = session['username']
            return redirect(url_for('route_panel'))
        else:
            return redirect(url_for('route_login'))

@app.route('/login' ,methods=['GET', 'POST'])
def route_login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        db_data = dbsearch(email)
        dbemail = db_data[0]['Email']
        dbpassword = db_data[0]['Password']
        global username
        username = db_data[0]['Username']
        if email == dbemail and password == dbpassword:
            session['username']= username
            return redirect(url_for('route_panel'))
        else:
            return redirect(url_for('route_wrongCredentials'))

    else:
        return render_template('login.html',classactive = 'd-none')


@app.route('/panel')
def route_panel():
    if 'username' in session:
        username = session['username']
        db_data = dbservers()
        print(db_data)
        return render_template('panel.html',data=db_data)
    else:
        return redirect(url_for('route_notlogin'))

@app.route('/profile')
def route_profile():
    if 'username' in session:
        username = session['username']
        print(username)
        return render_template('profile.html')
    else:
        return redirect(url_for('route_notlogin'))


@app.route('/wrongCredentials')
def route_wrongCredentials():
    return render_template('login.html', classactive = '.d-none')

@app.route('/Notlogin')
def route_notlogin():

    return render_template('login.html', classactive = '.d-none')


@app.route('/logout')
def route_logout():
    session.pop('username', None)
    return redirect(url_for('route_index'))


@app.route('/<string:name>/<string:task>/')
def route_quickactions(name,task):
    return "restarting" + name + task






if __name__ == "__main__":
    app.run(debug=True)
