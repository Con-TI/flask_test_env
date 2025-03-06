import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils import shuffle_deck, evaluate_winner
from botlogic import BotHardCoded

GLOBAL_STATE = {}

app = Flask(__name__)
app.secret_key = "poker_secret"

@app.route("/")
def home():
    return render_template("game.html")

@app.route("/create_deck", methods=["GET"])
def create_deck():
    deck = [{"rank":card[0],"suit":card[1]} for card in shuffle_deck()]
    return jsonify(deck)

@app.route("/get_bot_action", methods=["GET"])
def get_bot_action():
    bot_hand_str = eval(request.args.get('bot_hand'))
    community_cards_str = eval(request.args.get('community_cards'))
    pot = int(request.args.get('pot'))
    player_bet = int(request.args.get('player_bet'))
    opponent_bet = int(request.args.get('opponent_bet'))
    bot_hand = convert_hand(bot_hand_str)
    community_cards = convert_hand(community_cards_str)
    
    bot = BotHardCoded() 
    response = bot.call_bet_fold(bot_hand,community_cards,player_bet,opponent_bet,pot,None)
    return jsonify({
            "action": response,
            "status": "success"
        })

@app.route("/send_data_to_bot", methods=["POST"])
def send_data_to_bot():
    # Defaults to a dict
    data = request.get_json()
    
    return "", 204

@app.route("/determine_winner", methods=["GET"])
def determine_winner():
    player_hand_str = eval(request.args.get('player_hand'))
    bot_hand_str = eval(request.args.get('bot_hand'))
    community_cards_str = eval(request.args.get('community_cards'))

    player_hand = convert_hand(player_hand_str)
    bot_hand = convert_hand(bot_hand_str)
    community_cards = convert_hand(community_cards_str)
    
    winner = evaluate_winner(player_hand, bot_hand, community_cards)
    return jsonify({
            "winner": winner,
            "status": "success"
        })

def convert_hand(hand):
    return [card['rank']+card['suit'] for card in hand]
    

if __name__ == "__main__":
    app.run(debug=True)
