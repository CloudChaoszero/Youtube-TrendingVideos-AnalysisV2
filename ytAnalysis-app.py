from flask import Flask

from flask import jsonify, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
engine = create_engine("sqlite:///database.sqlite", echo=False)

from sqlalchemy import inspect
print(inspect(engine).get_table_names())

Base.prepare(engine, reflect = True)

from sqlalchemy.orm import Session


# Session.bind = engine 
session = Session(engine)
# session = Session.configure(bind=self.engine)
ytVideoStats = Base.classes.youtube_videoStats

app = Flask(__name__, template_folder = "Resources/templates")

@app.route("/")
def homepage():
    return(render_template("index.html"))


@app.route("/query")
def query():
    
    a = session.query(ytVideoStats).all()
    for i in a:
        print(i.videoID)
    return(f"{a}")

if __name__ == "__main__":
    app.run()