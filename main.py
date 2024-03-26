from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://master:as24rH0kpoMF4JOI@gamedb.xbxvq8z.mongodb.net/?retryWrites=true&w=majority&appName=GameDB")
db = client.game
player = db.player
games = db.games
current = False

@app.route('/', methods=['GET', 'POST'])
def login():
    global current
    if request.method == 'POST':
        if 'login' in request.form:
            username = request.form['username']
            password = request.form['password']
            current = player.find_one({"Name": username, "Password": password})
            if current:
                if current["Master"]:
                    return redirect(url_for('menu'))
                else:
                    return redirect(url_for('menu'))
            else:
                return render_template('login.html', error="Falscher Benutzername oder falsches Passwort")
        elif 'register' in request.form:
            username = request.form['username']
            password = request.form['password']
            if player.find_one({"Name": username}):
                return render_template('login.html', error="Der Name ist bereits vergeben")
            elif len(username) < 3 or len(password) < 3:
                return render_template('login.html', error="Benutzername oder Passwort zu kurz")
            else:
                player.insert_one({"Name": username, "Password": password, "Chips": 1000, "Master": False})
                current = player.find_one({"Name": username})
                return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global current
    if current:
        if current["Master"]:
            return render_template('menu.html', name=current["Name"],master=True)
        else:
            return render_template('menu.html', name=current["Name"])
    else:
        return redirect(url_for('login'))

@app.route('/bj_solo')
def bj_solo():
    return "Blackjack Solo"

@app.route('/bj_create')
def bj_create():
  return render_template("bj_create.html")

@app.route('/bj_join')
def bj_join():
    return render_template("bj_join.html")
@app.route('/vorlage')
def vorlage():
  return render_template('vorlage.html')
@app.route('/management')
def management():
    global current
    if current and current["Master"]:
        users = player.find()
        return render_template('management.html', users=users)
    else:
        return redirect(url_for('login'))

@app.route('/edit_user/<username>', methods=['GET', 'POST'])
def edit_user(username):
    if request.method == 'POST':
        name = request.form["name"]
        if(player.find_one({"Name":name}) and name != username):
          user = player.find_one({"Name": username})
          return render_template("edit_user.html",user=user,error = "Der Name ist bereits vergeben")
        password = request.form['password']
        chips = int(request.form['chips'])
        master = True if request.form['master'] == 'yes' else False
        player.update_one({"Name": username}, {"$set": {"Name":name,"Password": password, "Chips": chips, "Master": master}})
        return redirect(url_for('management'))
    user = player.find_one({"Name": username})
    return render_template('edit_user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
