from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secure session data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    player_count = int(request.form["players"])
    game_time = int(request.form["time"]) * 60  # Convert minutes to seconds

    session["player_count"] = player_count
    session["roles"] = assign_roles(player_count)
    session["current_player"] = 0
    session["start_time"] = time.time()
    session["game_time"] = game_time
    return redirect(url_for("show_role"))

@app.route("/show_role")
def show_role():
    current_player = session["current_player"]
    
    # Check if the game time has elapsed
    elapsed_time = time.time() - session["start_time"]
    if elapsed_time > session["game_time"]:
        flash("Game over! Time's up!")
        return redirect(url_for("results"))

    if current_player >= session["player_count"]:
        return redirect(url_for("results"))

    role = session["roles"][current_player]
    session["current_player"] += 1
    return render_template("role.html", role=role, player=current_player + 1)

@app.route("/results")
def results():
    return render_template("results.html")

def assign_roles(player_count):
    common_word = "Apple"  # Change dynamically if needed
    roles = [common_word] * player_count
    spy_index = random.randint(0, player_count - 1)  # Randomly select the Spy
    roles[spy_index] = "Spy"
    return roles

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)