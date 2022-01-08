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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ip',methods=['GET'])
def ip_query():
    return render_template('ip_query.html')

@app.route('/ip',methods=['POST'])
def ip_result():
    if request.method =='POST':
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root',
                                password='1234', port=3306, db='first')
            cur = conn.cursor()
            sql = "SELECT room,ip,flow,date from test_crawler where ip='" + \
                str(request.form.get('ip')) + "';"
            cur.execute(sql)
            u = cur.fetchall()
            conn.close()
            return render_template('ip_result.html', u=u, ip=request.form.get('ip'))
        except Exception as e:
            return render_template('error.html')

@app.route('/room',methods=['GET'])
def room_query():
    return render_template('room_query.html')

@app.route('/room',methods=['POST'])
def room_result():
    if request.method =='POST':
        try:
            conn = pymysql.connect(host='127.0.0.1', user='root',
                                password='1234', port=3306, db='first')
            cur = conn.cursor()
            sql = "SELECT room,ip,flow,date from test_crawler where room='" + \
                str(request.form.get('room')) + "';"
            cur.execute(sql)
            u = cur.fetchall()
            conn.close()
            return render_template('ip_result.html', u=u, ip=request.form.get('room'))
            # https://chilunhuang.github.io/posts/39347/ except handling
        except Exception as e:
            return render_template('error.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/feedback',methods=['GET'])
def feedback():
    return render_template('feedback.html')

@app.route('/feedback',methods=['POST'])
def feedback_result():
    return render_template('feedback_result.html')


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
