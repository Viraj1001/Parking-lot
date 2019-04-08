#Program written by Viraj Mishra

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,url_for
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query,relationship, backref

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parkdetails.db'
db = SQLAlchemy(app)

#Connecting the existing database
engine = create_engine('sqlite:///parkdetails.db', convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=True,autoflush=True,bind=engine))
meta=MetaData()
Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.reflect(engine)


 

class Parkingclass(Base):
    __table__ = Base.metadata.tables['parkinfo']



#Defining the home page and all its functionalities 
@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
        data=[]
        colours=[]
        for i,j in db_session.query(Parkingclass.spotId,Parkingclass.colour):
            data.append(i)
            colours.append(j)

        size=len(data)
        frcount=0
        bcount=0
        hcount=0
        facount=0
        for i in colours:
            if (i==0)|(i==3):
                frcount+=1
            if i==1:
                bcount+=1
            if i==3:
                hcount+=1
            if i==2:
                facount+=1

        selectedo =request.args.get('booking')
        updated = db_session.query(Parkingclass).filter_by(spotId=selectedo).update(dict(colour=1))
        db.session.commit()

        



        return render_template('home.html', title='Car Park',selected=selectedo, data=data,colours=colours,size=size,frcount=frcount,bcount=bcount,hcount=hcount,facount=facount)