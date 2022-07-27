from flask import Flask, request, render_template, redirect, session
import sqlite3
from helpers import random_str, get_timestamp, BASE_URL

app = Flask(__name__)

conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":

    if not request.form.get("url"):
      return "Please fill out all required field(s)"

    auto_code = random_str()
    codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code or code=:auto_code", {
      "auto_code": auto_code
    }).fetchall()

    while len(codes) != 0:
      auto_code = random_str()
      codes = c.execute("SELECT * FROM urls WHERE auto_code=:auto_code or code=:auto_code", {
        "auto_code": auto_code
      }).fetchall()

    date, time = get_timestamp()
    
    c.execute("INSERT INTO urls (original_url, auto_code, code, date, timestamp, user_id, click) VALUES (:o_url, :code, :code, :date, :time, :u_id, 0)", {
      "o_url": request.form.get("url"),
      "code": auto_code, 
      "date": date,
      "time": time,
      "u_id": session.get("user_id")
    })
    conn.commit()

    if session.get("user_id"):
      return render_template("confirm.html")
    return render_template("success.html", BASE_URL=BASE_URL, auto_code=auto_code, old=request.form.get("url"))

  else:
    return render_template("index.html")

@app.route("/url/<string:code>")
def url(code):
  result = c.execute("SELECT * FROM urls WHERE code=:code", {"code": code}).fetchall()
  if len(result) != 1:
    return "404"

  c.execute("UPDATE urls SET click = :c WHERE id=:id", {
    "c": int(result[0][7]) + 1,
    "id": result[0][0]
  })
  conn.commit()

  return redirect(result[0][1])
  
app.run(host='0.0.0.0', port=81)