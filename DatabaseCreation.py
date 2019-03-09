'''
Instatiating database via SQLAlchemy
by Raul Maldonado
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import csv
import os

# If Data folder does not exist, create it.
if os.path.exists('Data') is False:
    print("Creating Data Directory. :)")
    os.makedirs("Data")   
    os.makedirs("Data/Databases")   

#Decalarative Base class definition used for producing object representation 
# of table, and handle lf abstraction between the two.
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
    RegionCode = Column(String)
    Date = Column(String)

    def __repr__(self):
        return(f"<Youtube Video Information: Video Id: {self.videoID}, " + 
        f"Title: {self.title}, Published At: {self.publishedAt}, " + \
        f"Channel ID: {self.channelID}, Description: {self.description}, " + 
        f"Channel Title: {self.channelTitle}, Category ID: {self.categoryId}, " + 
        f"Region Code: {self.RegionCode}, Date: {self.Date}")

# Return value is instance of Engine API to connect and work with database
engine = create_engine('sqlite:///Data/Databases/database.sqlite')
ytVideoStats.__table__.drop(engine)
Base.metadata.create_all(engine, checkfirst=True)

# sessionmaker handles mapped objects to database
Session = sessionmaker(bind=engine)
session = Session()

'''
For each file, get open a csv and add the information to the intermediate table.
commit the file, and then go through to the next file
'''
counter = 0
fileDirectory = [i for i in os.listdir("Data/") if i != "Databases"]
for files in fileDirectory:

    with open(f'Data/{files}', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ytVids = ytVideoStats(id=counter, videoID=row[1], title=row[2], publishedAt=row[3],
                                  channelID=row[4], description=row[5], channelTitle=row[6],
                                  categoryId=row[7], viewCount=row[8], likeCount=row[9], 
                                  dislikeCount=row[10], favoriteCount=row[11], 
                                  commentCount=row[12], RegionCode=row[13], Date=row[14])
            session.add(ytVids)
            counter += 1
    
    session.query(ytVideoStats).filter(
        ytVideoStats.videoID == 'VideoID').delete()

    try:
        session.commit()
        print(session.query(ytVideoStats.videoID).all())
    except:
        ytVideoStats.__table__.drop(engine)
        print("Table was dropped due to duplicate IDs")
