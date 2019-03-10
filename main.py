# Flask and SQLAlchemy Dependencies
from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect
from sqlalchemy.orm import Session

import os
os.system('python DatabaseCreation.py')

Base = automap_base()
engine = create_engine("sqlite:///Data/Databases/database.sqlite",
                       connect_args={'check_same_thread': False}, echo=False)

Base.prepare(engine, reflect=True)
# print(inspect(engine).get_table_names()) #If I want to check out what table is available

session = Session(engine)
ytVideoStats = Base.classes.youtube_videoStats
'''
* Instantiate Flask object with all template resources in certain 
  location (default always lies in templates/).
    * Homepage instantiated at route "/". Receives text/html.
    * Search Page declared with returned .html file
    * Testing query page
    * Password page (Joke)
'''
from flask import Flask, render_template, redirect, request
app = Flask(__name__, template_folder="Resources/templates")
@app.route("/")
def homepage():
    return(render_template('index-home.html'))

@app.route("/analytics")
def analytics():
    ##First Idea (deprecated):
    # analytics_results = {}
    # analytics_results["StatsByCategoryID"] = session.query(ytVideoStats, \
    #     func.count(ytVideoStats.viewCount)).group_by(ytVideoStats.categoryId).all()
    #return(str(analytics_results))
    return(render_template('analytics.html'))
@app.route("/search", methods=['GET', 'POST'])
def searchPage():
    resultsNone = [  ["" for i in range(13)] for j in range(1) ]
    if request.method == "POST":
        querySearchForm = request.form["text"]
        results = session.query(ytVideoStats).filter(ytVideoStats.title.like(\
            f'%{querySearchForm}%')).all()
        
        results_list = [[row.videoID,row.title,row.publishedAt,row.channelID,\
                        row.channelTitle, row.categoryId, row.viewCount,\
                        row.likeCount, row.dislikeCount, row.favoriteCount,\
                        row.commentCount, row.RegionCode, row.Date] for row in results]

        return(render_template("index.html", output=results_list))
    return(render_template("index.html", output =resultsNone))
    

@app.route("/query", methods=['GET', 'POST'])
#youtube_videoStats table
def query():
    resultsNone = []
    if request.method == "POST":
        querySearchForm = request.form["text"]
       
        try:
            results_object = engine.execute(querySearchForm)
            results_column = tuple(results_object.keys())
            results = results_object.fetchall()
            results.insert(0, results_column)
        except:
            results = []
        results_list = results
        return(render_template("dynamic-query.html", output=results_list))
    return(render_template("dynamic-query.html", output =resultsNone))

@app.route("/password")
def password():
    return(render_template("password.html"))

if __name__ == "__main__":
    app.run()
