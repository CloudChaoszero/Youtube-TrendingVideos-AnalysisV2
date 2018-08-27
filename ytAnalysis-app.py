# Flask and SQLAlchemy Dependencies
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

'''
* Instantiate Flask object with all template resources in certain location (default always lies in templates/)
    * Homepage instantiated at route "/". Receives text/html related items to render to webpage
    * Search Page declared with returned .html file
    * Testing query page
    * Password page is possible
'''
from flask import Flask, render_template, redirect, request
app = Flask(__name__, template_folder="Resources/templates")
@app.route("/")
def homepage():
    return(render_template('index-home.html'))

@app.route("/demo")
def demo():
    return('''<h1>Welcome! :D </h1> <img src="https://i.kym-cdn.com/photos/images/newsfeed/000/415/209/3b4.png" alt="OKayyy" width="1100" height="1000"
    border="0">''')

@app.route("/search", methods=['GET', 'POST'])
def searchPage():
    resultsNone = [  ["" for i in range(13)] for j in range(1) ]
    if request.method == 'POST':
        querySearchForm = request.form['text']

        results = session.query(ytVideoStats).filter(
            ytVideoStats.title.like(f'%{querySearchForm}%')).all()
        print("Results: ", results)
        results_list = [[row.videoID,row.title,row.publishedAt,row.channelID,\
                        row.channelTitle,row.categoryId,row.viewCount,\
                        row.likeCount, row.dislikeCount,row.favoriteCount,row.commentCount, row.RegionCode, row.Date] for row in results]

        return(render_template("index.html", output=results_list))
    return(render_template("index.html", output =resultsNone))
    

@app.route("/query")
def query():

    return("Test Query")

@app.route("/password")
def password():
    return(render_template("password.html"))

if __name__ == "__main__":
    app.run()
