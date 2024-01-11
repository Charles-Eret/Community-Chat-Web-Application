from flask import Flask, request, redirect
from replit import db
import datetime,os
app = Flask(__name__)

f = open("template.html","r")
template = f.read()
f.close()
def getChat():
  chat = ""
  for key in list(db.keys()):
    post = template
    post = post.replace("{username}",db[key]["username"])
    post = post.replace("{timestamp}",key)
    post = post.replace("{message}",db[key]["message"])
    #if specified individual
    if request.headers["X-Replit-User-Id"] == os.getenv("myID"):
      #allows individual to delete posts
      post = post.replace("{admin}",f"""<a href="/delete?id={key}">❌</a>""")
    else:
      post = post.replace("{admin}","")
    chat += post
  return chat

@app.route("/")
def chat():
  f = open("chat.html","r")
  page = f.read()
  f.close()
  #if not logged in through replit
  if request.headers["X-Replit-User-Name"] == "":
    page = page.replace("{button}","""<button onclick="LoginWithReplit()"> Login </button>""")
    page = page.replace("{username}","guest")
    page = page.replace("{post}","")
  #if logged in through replit
  else:
    page = page.replace("{button}","")
    page = page.replace("{username}",request.headers["X-Replit-User-Name"])
    page = page.replace("{post}","""
  <form method="post" action="/add">
    <p>Mesage: <input type="text" name="message" required></p>
    <button type="submit">Post</button>
  </form>""")
  page = page.replace("{chat}",getChat())
  return page

@app.route("/add",methods=["POST"])
def add():
  if request.headers["X-Replit-User-Name"] == "":
    return redirect("/")
  form = request.form
  date = datetime.datetime.now()
  timestamp = datetime.datetime.timestamp(date)
  db[timestamp] = {"username":request.headers["X-Replit-User-Name"],"id":request.headers["X-Replit-User-Id"],"message":form["message"]}
  return redirect("/")

@app.route("/delete",methods=["GET"])
def delete():
  if request.headers["X-Replit-User-Id"] != os.getenv("myID"):
    return redirect("/")
  id = request.values["id"]
  del db[id]
  return redirect("/")

app.run(host='0.0.0.0', port=81)
