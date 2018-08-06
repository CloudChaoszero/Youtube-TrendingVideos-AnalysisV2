from flask import Flask

from flask import jsonify, render_template
import sqlalchemy

app = Flask(__name__, template_folder = "Resources/templates")

@app.route("/")
def homepage():
    return(render_template("index.html"))

if __name__ == "__main__":
    app.run()