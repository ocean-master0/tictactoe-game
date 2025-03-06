# Tic Tac Toe Game

## Project Overview
Tic Tac Toe is a sophisticated single-player web application developed using Flask, a lightweight Python web framework. This project reimagines the classic game with a modern twist, pitting players against a computer opponent with adjustable difficulty levels. Designed with a sleek, user-friendly interface, it incorporates advanced features like power-ups, real-time leaderboard updates, and dynamic gameplay elements, making it both entertaining and technically impressive. Deployable on cloud platforms, this game exemplifies a blend of elegant design and robust functionality.

## Features
- **Customizable Gameplay**:
  - **Board Sizes**: Supports 3x3 and 4x4 grids, catering to different skill levels.
  - **Difficulty Levels**: Offers Easy, Medium, and Hard modes, with Hard mode leveraging the Minimax algorithm for optimal AI moves.
  - **Win Conditions**: Players can choose between traditional row-based wins or a 2x2 square condition on larger boards.
- **Power-Ups**: Introduces strategic depth with three unique abilities:
  - *Clear Cell*: Removes a symbol from any cell.
  - *Swap Symbol*: Exchanges player and computer symbols.
  - *Double Move*: Allows two consecutive turns.
- **Real-Time Leaderboard**: Persistently tracks player wins and total games, updating instantly upon game completion.
- **Achievements System**: Rewards players for Hard mode victories and power-up usage, enhancing engagement.
- **Timed Gameplay**: Implements a 10-second move timer to heighten challenge and excitement.
- **Random Events**: Every fifth move triggers a random effect (board rotation or cell clearing), adding unpredictability.
- **UI/UX Design**:
  - Modern aesthetic with a purple-coral-yellow color scheme and neumorphic elements.
  - Light/dark theme toggle with persistent storage via `localStorage`.
  - Customizable board themes: Default, Space, and Jungle.
  - Professionally designed logo integrated as a favicon and beside the title.
- **Responsive Design**: Fully optimized for desktop and mobile devices.

## Technology Stack
- **Backend**: Flask (Python) handles game logic, state management, and API endpoints.
- **Frontend**:
  - HTML5 for structure.
  - CSS3 with gradients, neumorphism, and animations for styling.
  - JavaScript for dynamic interactions and real-time updates.
- **File Management**: JSON-based leaderboard persistence (`leaderboard.json`).
- **Assets**: Custom logo stored in `static/images/`.

## Project Structure
```
tictactoe_game/
├── static/
│   ├── images/
│   │   └── logo.png        # Game logo
│   ├── script.js          # Client-side logic
│   └── style.css          # Styling
├── templates/
│   └── index.html         # Main page
├── app.py                 # Flask application
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Installation (Local Development)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ocean-master0/tictactoe-game.git
   cd tictactoe-game
   ```
2. **Set Up Environment**:
   - Ensure Python 3.8+ is installed.
   - (Optional) Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # Linux/Mac
     venv\Scripts\activate     # Windows
     ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - Requires `Flask` and `gunicorn` (for deployment).
4. **Run the Application**:
   ```bash
   python app.py
   ```
   - Access at `http://127.0.0.1:5000` in your browser.

## Usage
- Launch the game, enter your name, and select your symbol (X or O).
- Choose board size, difficulty, and win condition, then start playing.
- Use power-ups strategically and watch the leaderboard update after each game.
- Toggle themes and enjoy random events that keep every match exciting.

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Report bugs or suggest improvements via GitHub Issues.

## License
This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute it.

## Live Demo
[Play Now](https://tictactoe-game-8.onrender.com)

## Author
- **Ocean Master**  
  GitHub: [ocean-master0](https://github.com/ocean-master0)
