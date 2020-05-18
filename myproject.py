from flask import Flask
from flask import redirect, url_for, request, render_template, Response
from flask import jsonify
import mysql.connector
import hashlib
from flask_cors import CORS, cross_origin
import datetime
import json
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

@app.route('/isAdmin')
@cross_origin()
def isAdmin():
    return ''

@app.route('/isAdmin/<string:username>', methods=['GET', 'POST'])
@cross_origin()
def admin_check(username):
    cnx = None
    cnx = mysql.connector.connect(user=db['user'], password=db['password'], host=db['host'], database=db['database'])
    print('Connected', cnx)
    if request.method == 'GET':
        cursor = cnx.cursor()
        #print(username)
        query = f"SELECT user_name, user_type from user WHERE user_name='{username}' and user_type='admin'"
        cursor.execute(query)
        x = []
        for elem in cursor:
            x.append(elem)
        if len(x) == 0:
            data = {'isAdmin':False}
        else:
            data = ({'isAdmin':True})

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )

        return response

@app.route('/admission', methods=['GET', 'POST'])
@cross_origin()
def admission():
    cnx = None
    cnx = mysql.connector.connect(user=db['user'], password=db['password'], host=db['host'], database=db['database'])
    #print('Connected', cnx)
    if request.method == 'GET':
        return render_template('admission.html')
    if request.method == 'POST':
        data = {}
        #print(request.form)
        for key in request.form.keys():
            data[key] = request.form[key]
        response = Response()
        cursor = cnx.cursor()
        ts = hash(str(datetime.datetime.now().timestamp()))[:8].upper()
        data['birthday'] = datetime.datetime.strptime(data['birthday'], '%d/%m/%Y').strftime('%Y-%m-%d')
        query = f"""INSERT INTO new_avedata.admissions
                (id, first_name, last_name, gender, standard, dob, email, phone, alt_phone, mother_name, father_name, address1, address2, area, schoolID)
                VALUES('{ts}', '{data['first_name']}', '{data['last_name']}', '{data['gender']}', '{data['standard']}', '{data['birthday']}', '{data['email']}',
                '{data['phone']}', '{data['alt_phone']}', '{data['mother_name']}', '{data['father_name']}', '{data['address1']},',
                '{data['address2']}', '{data['area']}', '{data['schoolID']}');"""
        cursor.execute(query)
        cnx.commit()
        print('Record inserted.')
        return f'<h1>Please note : </h1><h2>Admission Request Code : <mark>{ts}</mark></h2><br><p>Form Submitted, wait for request approval. <a href="http://www.avelearning.in/">Click Here</a> to return to Home Page</p>'      

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
    cnx = None
    cnx = mysql.connector.connect(user=db['user'], password=db['password'], host=db['host'], database=db['database'])
    #print('Connected', cnx)
    if request.method == 'POST':
        response = Response()
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
    
@app.route('/requests', methods=['GET', 'POST'])
@cross_origin()
def requests():
    cnx = None
    cnx = mysql.connector.connect(user=db['user'], password=db['password'], host=db['host'], database=db['database'])
    #print('Connected', cnx)
    if request.method == 'GET':
        query = '''SELECT id, first_name, last_name, dob, gender, standard, schoolID, email,phone, alt_phone, mother_name, father_name, address1, address2, area, city, state from admissions'''
        response = Response()
        cursor = cnx.cursor()
        cursor.execute(query)
        if cursor.rowcount == 0:
            response.status_code = 400
            response.data = render_template('error.html', error_data="User doesn't exist.")
        
        data_list = []
        for data in cursor:
            data_list.append(data)
        response.status_code = 200
        response.data = render_template('requests.html', data_list = data_list)
        return response

if __name__ == '__main__':
    app.run(debug=True)