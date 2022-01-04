import re
from flask import *
from os import *
from flask_sqlalchemy import *
from pymysql import *
import pymysql

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/first"
db.init_app(app)


@app.route('/')
def index():
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           password='1234', port=3306, db='first')
    cur = conn.cursor()
    sql = "SELECT room,ip,flow,date from test_crawler where room='6401D';"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('query.html', u=u)


@app.route('/room/<room>')
def room_query(room):
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root',
                               password='1234', port=3306, db='first')
        cur = conn.cursor()
        sql = "SELECT room,ip,flow,date from test_crawler where room='"+room+"';"
        cur.execute(sql)
        u = cur.fetchall()
        conn.close()
        return render_template('room_query.html', u=u, room=room)
    except Error:
        return error


@app.route('/ip/<ip>')
def ip_query(ip):
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           password='1234', port=3306, db='first')
    cur = conn.cursor()
    sql = "SELECT room,ip,flow,date from test_crawler where room='"+ip+"';"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('index.html', u=u, ip=ip)


@app.route('/db')
def dbb():
    sql_cmd = "SELECT room,flow from test_crawler where room='5101A';"
    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


@app.route('/query')
def query():
    return render_template('query.html')


@app.route("/", methods=['POST'])
def submit():
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root',
                               password='1234', port=3306, db='first')
        cur = conn.cursor()
        sql = "SELECT room,ip,flow,date from test_crawler where ip='" + \
            str(request.form.get('ip')) + "';"
        cur.execute(sql)
        u = cur.fetchall()
        conn.close()
        return render_template('ip_query.html', u=u, ip=request.form.get('ip'))
    return 'error'


@app.route("/", method=['GET'])
def hi():
    return "hi"


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


'''
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user_name:password@IP:3306/db_name"

db.init_app(app)

@app.route('/')
def index():

    sql_cmd = """
        select *
        from product
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


if __name__ == "__main__":
    app.run()
'''
