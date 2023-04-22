from flask import Flask, render_template
from connect_db import connect_PSQL
from fetch_db import fetch_sreality
from scrape import start_crawler

app = Flask(__name__)
connect_PSQL()
start_crawler()

@app.route("/")
def index():
    results = fetch_sreality()
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)