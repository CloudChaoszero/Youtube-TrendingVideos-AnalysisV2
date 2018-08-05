'''
Establishing database using SQLAlchemy

SQL Dialect: SQLite
            Used for in-memory database
'''
#ORM Model
#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html



#Return value is instance of Engine, represents core
#interface to database.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()

class ytVideoStats(Base):
    __tablename__ = "youtube_videoStats"
    id = Column(Integer, primary_key=True)
    videoID = Column(String)
    title = Column(String)
    publishedAt = Column(String)
    channelID = Column(String)
    description = Column(String)
    channelTitle = Column(String)
    categoryId = Column(Integer)
    viewCount = Column(Integer)
    likeCount = Column(Integer)
    dislikeCount = Column(Integer)
    favoriteCount = Column(Integer)
    commentCount = Column(Integer)
    def __repr__(self):
        return(f"<Youtube Video Information: Video Id: {self.videoID}, Title: {self.title}, Published At: {self.publishedAt},\
        Channel ID: {self.channelID}, Description: {self.description}, Channel Title: {self.channelTitle}, Category ID: {self.categoryId}")
ytVideoStats.__table__.drop(engine)
#Session: ORM's "handle" to the database
Base.metadata.create_all(engine, checkfirst=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind =engine)
session = Session()


import csv
counter = 0
with open('Data/YoutubeVideoStats-BE-832018.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        ytVids = ytVideoStats(id = counter, videoID=row[1], title = row[2], publishedAt=row[3],\
        channelID = row[4], description = row[5],channelTitle=row[6], categoryId=row[7],\
        viewCount=row[8],likeCount=row[9],dislikeCount=row[10],favoriteCount=row[11],commentCount=row[12])
        # Instance is pending. No SQL has been issued to object. To persist our object,
        # #we add it to our session 
        session.add(ytVids)
        counter +=1
try:
    session.commit()
    print(session.query(ytVideoStats.videoID).all())
except:
    ytVideoStats.__table__.drop(engine)
    print("Table was dropped due to duplicate IDs")


