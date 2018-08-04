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
    videoID = Column(String, primary_key = True)
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

#Session: ORM's "handle" to the database
Base.metadata.create_all(engine, checkfirst=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind =engine)
session = Session()


import csv
with open('Data/YoutubeVideoStats-BE-832018.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        print(row[1],"\n")
        ytVids = ytVideoStats(videoID=row[1], title = row[2], publishedAt=row[3],\
        channelID = row[4], description = row[5],channelTitle=row[6], categoryId=row[7],\
        viewCount=row[8],likeCount=row[9],dislikeCount=row[10],favoriteCount=row[11],commentCount=row[12])
        session.add(ytVids)
session.commit()
print(session.query(ytVideoStats.videoID).all())