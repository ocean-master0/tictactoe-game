from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Game state
game_data = {
    "player1_name": "",
    "player1_symbol": "X",
    "player2_symbol": "O",
    "winner": None,
    "draw": False,
    "board_size": 3,
    "player_score": 0,
    "computer_score": 0,
    "difficulty": "Medium",
    "move_count": 0,
    "achievements": {"hard_wins": 0},
    "win_condition": "row"
}
board = None

# Use absolute path for leaderboard file
leaderboard_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")

# Create leaderboard.json if it doesn't exist
try:
    if not os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'w') as f:
            json.dump({}, f)
except Exception as e:
    print(f"Error creating leaderboard file: {e}")

def initialize_board(size):
    global board
    board = [['' for _ in range(size)] for _ in range(size)]
    print(f"Initialized board: {board}")

def check_win(board, symbol, condition="row"):
    size = len(board)
    if condition == "row":
        for row in board:
            if all(cell == symbol for cell in row):
                return True
        for col in range(size):
            if all(board[row][col] == symbol for row in range(size)):
                return True
        if all(board[i][i] == symbol for i in range(size)):
            return True
        if all(board[i][size-1-i] == symbol for i in range(size)):
            return True
    elif condition == "square":
        for i in range(size-1):
            for j in range(size-1):
                if all(board[i+x][j+y] == symbol for x in range(2) for y in range(2)):
                    return True
    return False

def check_draw(board):
    return all(cell != '' for row in board for cell in row)

def get_computer_move(board, computer_symbol, player_symbol, difficulty):
    size = len(board)
    available_moves = [(i, j) for i in range(size) for j in range(size) if board[i][j] == '']
    if not available_moves:
        return None
    if difficulty == "Easy":
        return random.choice(available_moves)
    elif difficulty == "Medium":
        for i in range(size):
            for j in range(size):
                if board[i][j] == '':
                    board[i][j] = computer_symbol
                    if check_win(board, computer_symbol, game_data["win_condition"]):
                        board[i][j] = ''
                        return (i, j)
                    board[i][j] = ''
        for i in range(size):
            for j in range(size):
                if board[i][j] == '':
                    board[i][j] = player_symbol
                    if check_win(board, player_symbol, game_data["win_condition"]):
                        board[i][j] = ''
                        return (i, j)
                    board[i][j] = ''
        center = size // 2
        if board[center][center] == '':
            return (center, center)
        return random.choice(available_moves)
    elif difficulty == "Hard":
        def minimax(board, depth, is_maximizing):
            if check_win(board, computer_symbol, game_data["win_condition"]):
                return 10 - depth
            if check_win(board, player_symbol, game_data["win_condition"]):
                return depth - 10
            if check_draw(board):
                return 0
            if is_maximizing:
                best_score = -float('inf')
                for i in range(size):
                    for j in range(size):
                        if board[i][j] == '':
                            board[i][j] = computer_symbol
                            score = minimax(board, depth + 1, False)
                            board[i][j] = ''
                            best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for i in range(size):
                    for j in range(size):
                        if board[i][j] == '':
                            board[i][j] = player_symbol
                            score = minimax(board, depth + 1, True)
                            board[i][j] = ''
                            best_score = min(score, best_score)
                return best_score

        best_move = None
        best_score = -float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == '':
                    board[i][j] = computer_symbol
                    score = minimax(board, 0, False)
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

def random_event():
    global board
    if random.random() < 0.2:
        board = [list(row) for row in zip(*board[::-1])]
        return "Board rotated!"
    elif random.random() < 0.4:
        filled = [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] != '']
        if filled:
            i, j = random.choice(filled)
            board[i][j] = ''
            return f"Cell ({i}, {j}) cleared!"
    return None

def update_leaderboard():
    try:
        with open(leaderboard_file, 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = {}
    player = game_data["player1_name"]
    if player not in leaderboard:
        leaderboard[player] = {"wins": 0, "games": 0}
    leaderboard[player]["wins"] = game_data["player_score"]
    leaderboard[player]["games"] += 1
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f)
    return leaderboard  # Return updated leaderboard for real-time update

@app.route('/')
def index():
    global board
    initialize_board(game_data["board_size"])
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global board, game_data
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        player_name = data.get('player1_name', '').strip()
        if not player_name:
            return jsonify({"error": "Player name is required"}), 400
        
        game_data["player1_name"] = player_name
        game_data["player1_symbol"] = data.get('symbol', 'X')
        game_data["player2_symbol"] = 'O' if game_data["player1_symbol"] == 'X' else 'X'
        
        board_size = data.get('board_size', 3)
        if board_size not in [3, 4]:
            return jsonify({"error": "Board size must be 3 or 4"}), 400
        game_data["board_size"] = board_size
        
        difficulty = data.get('difficulty', 'Medium')
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            return jsonify({"error": "Invalid difficulty level"}), 400
        game_data["difficulty"] = difficulty
        
        win_condition = data.get('win_condition', 'row')
        if win_condition not in ['row', 'square']:
            return jsonify({"error": "Invalid win condition"}), 400
        game_data["win_condition"] = win_condition
        
        initialize_board(game_data["board_size"])
        print(f"Game started: board_size={game_data['board_size']}, board={board}")
        return jsonify(game_data)
    except Exception as e:
        print(f"Error starting game: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/make_move', methods=['POST'])
def make_move():
    global board, game_data
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        row, col = data.get('row'), data.get('col')
        
        # Validate row and col are not None
        if row is None or col is None:
            return jsonify({"error": "Row and column are required"}), 400
        
        print(f"Received move: row={row}, col={col}, board={board}")
        
        if not (0 <= row < game_data["board_size"] and 0 <= col < game_data["board_size"]):
            print(f"Out of bounds: row={row}, col={col}, board_size={game_data['board_size']}")
            return jsonify({"error": "Invalid move"}), 400
        if board[row][col] != '':
            print(f"Cell already taken: ({row}, {col}) = {board[row][col]}")
            return jsonify({"error": "Invalid move"}), 400

        board[row][col] = game_data["player1_symbol"]
        game_data["move_count"] += 1
    except (TypeError, ValueError) as e:
        print(f"Error processing move: {e}")
        return jsonify({"error": "Invalid move data"}), 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    if check_win(board, game_data["player1_symbol"], game_data["win_condition"]):
        game_data["winner"] = game_data["player1_name"]
        game_data["player_score"] += 1
        if game_data["difficulty"] == "Hard":
            game_data["achievements"]["hard_wins"] += 1
        leaderboard = update_leaderboard()
        return jsonify({"board": board, "winner": game_data["winner"], "draw": False, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"], "leaderboard": leaderboard})

    if check_draw(board):
        game_data["draw"] = True
        leaderboard = update_leaderboard()
        return jsonify({"board": board, "winner": None, "draw": True, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"], "leaderboard": leaderboard})

    if game_data["move_count"] % 5 == 0:
        event = random_event()
        if event:
            return jsonify({"board": board, "event": event})

    computer_move = get_computer_move(board, game_data["player2_symbol"], game_data["player1_symbol"], game_data["difficulty"])
    if computer_move:
        row, col = computer_move
        board[row][col] = game_data["player2_symbol"]
        game_data["move_count"] += 1
        if check_win(board, game_data["player2_symbol"], game_data["win_condition"]):
            game_data["winner"] = "Computer"
            game_data["computer_score"] += 1
            leaderboard = update_leaderboard()
            return jsonify({"board": board, "winner": game_data["winner"], "draw": False, "computer_move": {"row": row, "col": col}, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"], "leaderboard": leaderboard})
        if check_draw(board):
            game_data["draw"] = True
            leaderboard = update_leaderboard()
            return jsonify({"board": board, "winner": None, "draw": True, "computer_move": {"row": row, "col": col}, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"], "leaderboard": leaderboard})
        return jsonify({"board": board, "winner": None, "draw": False, "computer_move": {"row": row, "col": col}, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"]})
    return jsonify({"board": board})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        with open(leaderboard_file, 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        print("Leaderboard file not found, returning empty leaderboard")
        return jsonify({})
    except json.JSONDecodeError:
        print("Error decoding leaderboard JSON, returning empty leaderboard")
        return jsonify({})
    except Exception as e:
        print(f"Unexpected error reading leaderboard: {e}")
        return jsonify({})

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board, game_data
    initialize_board(game_data["board_size"])
    game_data["winner"] = None
    game_data["draw"] = False
    game_data["move_count"] = 0
    return jsonify({"message": "Game reset", "board": board, "scores": {"player": game_data["player_score"], "computer": game_data["computer_score"]}, "achievements": game_data["achievements"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000
    app.run(host='0.0.0.0', port=port, debug=False)