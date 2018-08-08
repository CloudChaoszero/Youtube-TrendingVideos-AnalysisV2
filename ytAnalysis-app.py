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
    if request.method == 'POST':
        querySearchForm = request.form['text']

        # // TODO: If all is well, take out test print statement from below
        print("Query Word:", querySearchForm)

        results = session.query(ytVideoStats).filter(
            ytVideoStats.title.like(f'%{querySearchForm}%')).all()

        results_list = [row.title for row in results]
        # // TODO: If all is well, take out test print statement from below
        print(results_list)
        return(render_template("index.html", output=results_list))
    return(render_template("index.html"))


@app.route("/query")
def query():

    # a = session.query(ytVideoStats).all()
    # listt = [i.videoID for i in a]
    # return(f"{listt}")
    return("das")

@app.route("/password")
def password():
    return(render_template("rickroll.html"))
if __name__ == "__main__":
    app.run()
