from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect
from sqlalchemy.orm import Session

Base = automap_base()
engine = create_engine("sqlite:///database.sqlite",
                       connect_args={'check_same_thread': False}, echo=False)

Base.prepare(engine, reflect=True)
# print(inspect(engine).get_table_names()) #If I want to check out what table is available

session = Session(engine)
ytVideoStats = Base.classes.youtube_videoStats

app = Flask(__name__, template_folder="Resources/templates")


@app.route("/")
def homepage():
    return("<h1>Welcome! :D </h1>")


@app.route("/search", methods=['GET', 'POST'])
def searchPage():
    resultsNone = [  ["" for i in range(13)] for j in range(1) ]
    if request.method == 'POST':
        querySearchForm = request.form['text']

        # // TODO: If all is well, take out test print statement from below
        #print("Query Word:", querySearchForm)

        results = session.query(ytVideoStats).filter(
            ytVideoStats.title.like(f'%{querySearchForm}%')).all()
        print("Results: ", results)
        results_list = [[row.videoID,row.title,row.publishedAt,row.channelID,\
                        row.channelTitle,row.categoryId,row.viewCount,\
                        row.likeCount, row.dislikeCount,row.favoriteCount,row.commentCount, row.RegionCode, row.Date] for row in results]
        # // TODO: If all is well, take out test print statement from below
        #print(results_list)
        
        return(render_template("index.html", output=results_list))
    return(render_template("index.html", output =resultsNone))


@app.route("/query")
def query():

    return("das")

@app.route("/password")
def password():
    return(render_template("password.html"))
if __name__ == "__main__":
    app.run()
