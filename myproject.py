from flask import Flask
from flask import redirect, url_for, request, render_template, Response
from flask import jsonify
import mysql.connector
import hashlib
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = {
    'user':'yatharth',
    'password':'12345',
    'host':'166.62.27.179',
    'database':'new_avedata',
}
def hash(string):
    return hashlib.md5(string.encode('utf8')).hexdigest()


@app.route('/admission', methods=['GET', 'POST'])
@cross_origin()
def admission():
    if request.method == 'GET':
        return render_template('admission.html')
    if request.method == 'POST':
        print(request.form)
        return f'Form Submitted, wait for request approval. <br><a href="http://www.avelearning.in/">Click Here</a> to return to Home Page'      

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def _dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@cross_origin()
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html')
    

@app.route("/login", methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        cnx = None
        response = Response()
        try:
            cnx = mysql.connector.connect(user=db['user'], password=db['password'], host=db['host'], database=db['database'])
        except mysql.connector.Error as e:
            response.status_code = 400
            response.data = render_template('error.html', error_data=e)
            return response
        #print(request.form)
        username = request.form['username']
        usertype = request.form['usertype']
        password_hash = hash(request.form['password'])
        cursor = cnx.cursor()
        query = f'SELECT user_name, password_hash, user_type FROM user WHERE user_name = "{username}"'

        cursor.execute(query)
        if cursor.rowcount == 0:
            response.status_code = 400
            response.data = render_template('error.html', error_data="User doesn't exist.")
            
        for _, phash, utype in cursor:
            if utype != usertype:
                response.status_code = 400
                response.data = render_template('error.html', error_data="Usertype is incorrect.")
            elif phash != password_hash:
                response.status_code = 400
                response.data = render_template('error.html', error_data="Password did not match.")
            else:
                response.status_code = 200
                return redirect(url_for('dashboard'))
        return response


    else:
        return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True)