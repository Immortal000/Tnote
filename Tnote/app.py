from flask import Flask ,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy 
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tmp/allnotes.db'
app.config['SECRET_KEY']='A secret key!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Notess(db.Model): 
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),unique=True)
	content = db.Column(db.String(1000))

@app.route('/')
def form():
	return render_template('index.html')

@app.route('/',methods=['POST'])
def view(): 
	title = request.form['title']
	content = request.form['content']
	check_url = Notess.query.filter_by(title=title).first()
	if check_url: 
		return render_template('view.html')
	else:
		note=Notess(title=title,content=content)
		db.session.add(note)
		db.session.commit()
		return redirect('http://127.0.0.1:5000/allnotes')

@app.route('/allnotes')
def allnotes():
	notes = Notess.query.all()
	return render_template('allnotes.html',notes=notes)

if __name__ == '__main__': 
	app.run(debug=True)