from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# List of words
WORDS = ["apple", "banana", "cherry", "dragonfruit", "elephant", "falcon"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    data = request.json
    num_players = int(data['num_players'])

    if num_players < 2:
        return jsonify({"error": "Number of players must be at least 2"}), 400

    word = random.choice(WORDS)  # Randomly select a word
    spy_index = random.randint(0, num_players - 1)  # Randomly select the spy

    players = [{"id": i + 1, "text": word if i != spy_index else "You are the Spy"} for i in range(num_players)]

    return jsonify({"players": players})

if __name__ == '__main__':
    app.run(debug=True)