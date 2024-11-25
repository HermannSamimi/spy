from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secure session data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", time=time())

@app.route("/start", methods=["POST"])
def start():
    player_count = int(request.form["players"])
    game_time = int(request.form["time"]) * 60  # Convert minutes to seconds

    session["player_count"] = player_count
    session["roles"] = assign_roles(player_count)
    session["current_player"] = 0
    session["start_time"] = time.time()
    session["game_time"] = game_time  # Store game time
    return redirect(url_for("show_role"))

@app.route("/show_role")
def show_role():
    current_player = session["current_player"]
    player_count = session["player_count"]

    if current_player >= player_count:
        # All players have seen their roles; timer will start on the same page
        return render_template(
            "role.html", role=None, player=None, all_roles_seen=True, game_time=session["game_time"]
        )

    role = session["roles"][current_player]
    session["current_player"] += 1
    return render_template("role.html", role=role, player=current_player + 1, all_roles_seen=False)

@app.route("/game_timer")
def game_timer():
    game_time = session.get("game_time", 300)  # Default to 5 minutes
    return render_template("game_timer.html", game_time=game_time)

@app.route("/results")
def results():
    # Retrieve game_time from the session
    game_time = session.get("game_time", 300)  # Default to 300 seconds (5 minutes)
    return render_template("results.html", game_time=game_time)

def assign_roles(player_count):
    common_word = "Apple"  # Change dynamically if needed
    roles = [common_word] * player_count
    spy_index = random.randint(0, player_count - 1)  # Randomly select the Spy
    roles[spy_index] = "Spy"
    return roles

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)