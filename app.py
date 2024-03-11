from flask import Flask,render_template,redirect,request,url_for
import sqlite3
app=Flask(__name__)
DATABASE= 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.execute('''CREATE TABLE IF NOT EXISTS contacts(
        id INTEGERPRIMARY KEY AUDIOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        number INTEGER NOT NULL,
        message TEXT NOT NULL
    )'''
    )
    db.commit()
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql' ,mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



@app.route("/")

def contact_form():
    return render_template('index.html')
@app.route('/submit',methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form[ 'name']
        email = request.form[ 'email']
        number = request.form[ 'number']
        message = request.form[ 'message']

        db = get_db()
        db.execute('INSERT INTO contacts (name,email,number,message) VALUES (?,?,?,?)', (name,email,number,message))
        db.commit()
        db.close()

        return redirect(url_for('thank'))

@app.route('/thank')
def thank():
    return render_template('thank.html')

@app.route('/')
def home():
    return render_template('index.html')
app.run(debug=True,port=5006)
