from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/commit")
def commit():
    # This is used when the arduino commits a users trash points
    return "TODO"

@app.route("/init")
def init_state():
    # This is used to init all users and reset the points if nessessary
    return "TODO"

@app.route("/scoreboard")
def scoreboard():
    # This is used to see the scoreboard with all the users and their points etc
    return "TODO"