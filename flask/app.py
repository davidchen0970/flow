from flask import *
from os import *
from flask_sqlalchemy import *
from pymysql import *
import pymysql
import mysql.connector
from mysql.connector import errorcode

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/first"
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/ip', methods=['GET'])
def ip_query():
    return render_template('ip_query.html')


@app.route('/ip', methods=['POST'])
def ip_result():
    if request.method == 'POST':
        try:
            config = {

                'host': 'david0970.mysql.database.azure.com',
                'user': 'david0970',
                'password': 'Apple1234',
                'database': 'first',
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
            }
            conn = mysql.connector.connect(**config)
            cur = conn.cursor()
            sql = "SELECT room,ip,flow,date from test_crawler where ip='" + \
                str(request.form.get('ip')) + "';"
            cur.execute(sql)
            u = cur.fetchall()
            conn.close()
            return render_template('ip_result.html', u=u, ip=request.form.get('ip'))
        except Exception as e:
            return render_template('error.html')


@app.route('/room', methods=['GET'])
def room_query():
    return render_template('room_query.html')


@app.route('/room', methods=['POST'])
def room_result():
    if request.method == 'POST':
        try:
            config = {

                'host': 'david0970.mysql.database.azure.com',
                'user': 'david0970',
                'password': 'Apple1234',
                'database': 'first',
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
            }
            conn = mysql.connector.connect(**config)
            cur = conn.cursor()
            sql = "SELECT room,ip,flow,date from test_crawler where room='" + \
                str(request.form.get('room')) + "';"
            cur.execute(sql)
            u = cur.fetchall()
            conn.close()
            return render_template('ip_result.html', u=u, ip=request.form.get('room'))
            # https://chilunhuang.github.io/posts/39347/ except handling
        except Exception as e:
            print(e)
            return render_template('error.html', e=e)


@app.route('/navbar')
def navbar():
    return render_template('navbar.html')


@app.route('/navbar_bottom')
def navbar_bottom():
    return render_template('navbar_bottom.html')


@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html')


@app.route('/feedback', methods=['POST'])
def feedback_result():
    if request.method == 'POST':
        try:
            config = {

                'host': 'david0970.mysql.database.azure.com',
                'user': 'david0970',
                'password': 'Apple1234',
                'database': 'first',
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
            }
            conn = mysql.connector.connect(**config)
            # https://blog.csdn.net/MATLAB_matlab/article/details/106197816
            feedback_name = str(request.form.get('feedback_name'))
            feedback_text = str(request.form.get('feedback_text'))
            feedback_phone = str(request.form.get('feedback_phone'))
            feedback_room = str(request.form.get('feedback_room'))

            cur = conn.cursor()
            sql = ("INSERT INTO `feedback` ( feedback_name,feedback_text,phonenumber ,room) VALUES ( \'" +
                   feedback_name + "\',\'" + feedback_text + "\',\'" + feedback_phone+"\',\'" + feedback_room+"\');")
            print(sql)
            cur.execute(sql)
            conn.commit()
            conn.close()
        except Exception as e:
            return render_template('feedback_result.html', result="error")
    return render_template('feedback_result.html',
                           result="success",
                           feedback_name=feedback_name,
                           feedback_text=feedback_text,
                           feedback_phone=feedback_phone,
                           feedback_room=feedback_room)


@app.route('/feedback/query', methods=['GET'])
def query_feedback():
    try:
        config = {

                'host': 'david0970.mysql.database.azure.com',
                'user': 'david0970',
                'password': 'Apple1234',
                'database': 'first',
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
            }
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()
        sql = "SELECT feedback_name,feedback_text,room from feedback ;"
        cur.execute(sql)
        u = cur.fetchall()
        conn.close()
        return render_template('feedback_query.html', u=u)
    except Exception as e:
        return render_template('error.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# https://medium.com/@charming_rust_oyster_221/flask-%E9%85%8D%E7%BD%AE-https-%E7%B6%B2%E7%AB%99-ssl-%E5%AE%89%E5%85%A8%E8%AA%8D%E8%AD%89-36dfeb609fa8
# SSL ???????????? (HTTPS)
