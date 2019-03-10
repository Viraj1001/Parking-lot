#Program written by Viraj Mishra

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,url_for
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parkdetails.db'
db = SQLAlchemy(app)

#Connecting the existing database
engine = create_engine('sqlite:///parkdetails.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref

class Parkingclass(Base):
    __table__ = Base.metadata.tables['parkinfo']


#Defining the home page and all its functionalities 
@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
	connection=db.engine.raw_connection()
	cur = connection.cursor()
	cur.execute("SELECT spotId FROM parkinfo")
	data = cur.fetchall()
	cur1=connection.cursor()
	cur1.execute("SELECT colour FROM parkinfo")
	colours=cur1.fetchall();
	size=len(data)  #number of parking spots
	frcount=0       #number of open spots
	bcount=0		#number of booked spots
	hcount=0		#number of handicap spots
	facount=0		#number of faculty spots


	for i in colours:
		if (i==(0,))|(i==(3,)):
			frcount+=1
		if i==(1,):
			bcount+=1
		if i==(3,):
			hcount+=1
		if i==(2,):
			facount+=1

	selected0 =str(request.form.get('booking'))   #selected spot to be booked

	cur2=connection.cursor()
	query="""Update parkinfo set colour='1' WHERE spotId = '%s' """ % (selected0)
	bookrow=cur2.execute(query)
	db.session.commit()

	return render_template('home.html', title='Car Park',selected=(selected0), data=data,colours=colours,size=size,frcount=frcount,bcount=bcount,hcount=hcount,facount=facount)