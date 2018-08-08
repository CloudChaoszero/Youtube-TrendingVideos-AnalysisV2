from flask import Flask, render_template, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect
from sqlalchemy.orm import Session

Base = automap_base()
engine = create_engine("sqlite:///database.sqlite", connect_args={'check_same_thread': False},echo=False)

Base.prepare(engine, reflect = True)
# print(inspect(engine).get_table_names())

session = Session(engine)
ytVideoStats = Base.classes.youtube_videoStats

#Application instance
app = Flask(__name__, template_folder = "Resources/templates")

@app.route("/")
def homepage():
    return("<h1>Welcome! :D </h1>")

@app.route("/search", methods = ['Get','POST'])
def searchPage():
    if request.method == 'POST':
        queryWord = request.form['text']
        print("Query Word:", queryWord)
        a = session.query(ytVideoStats.title).filter(ytVideoStats.title.like(f'%{queryWord}%')).all()

        listt = [i for i in a]
        print(listt)
        return(render_template("index.html", aye = listt))
    return(render_template("index.html"))


@app.route("/query")
def query():
    
    # a = session.query(ytVideoStats).all()
    # listt = [i.videoID for i in a]
    # return(f"{listt}")
    return("das")
if __name__ == "__main__":
    app.run()

'''
Want to be able to query video information by
some video category, id, or something else
through some submission html page
'''

'''
Currently have ability to query video ids as a whole
'''

# http://flask.pocoo.org/docs/0.12/quickstart/