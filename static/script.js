let playerName = '';
let playerSymbol = '';
let computerSymbol = '';
let isGameActive = true;
let boardSize = 3;
let timeLeft = 10;
let timer = null;

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const nameEntry = document.getElementById('name-entry');
    const symbolSelection = document.getElementById('symbol-selection');
    const gameBoard = document.getElementById('game-board');
    const resetButton = document.getElementById('reset-button');
    const themeToggle = document.getElementById('theme-toggle');
    const themeSelect = document.getElementById('theme-select');

    startButton.addEventListener('click', () => {
        playerName = document.getElementById('player1_name').value.trim();
        boardSize = parseInt(document.getElementById('board-size').value);
        if (playerName) {
            nameEntry.style.display = 'none';
            symbolSelection.style.display = 'block';
            document.getElementById('symbol-prompt').textContent = `${playerName}, choose your symbol:`;
        } else {
            alert('Please enter your name');
        }
    });

    document.querySelectorAll('.symbol-button').forEach(button => {
        button.addEventListener('click', () => {
            playerSymbol = button.dataset.symbol;
            computerSymbol = playerSymbol === 'X' ? 'O' : 'X';
            fetch('/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    player1_name: playerName,
                    symbol: playerSymbol,
                    board_size: boardSize,
                    difficulty: document.getElementById('difficulty').value,
                    win_condition: document.getElementById('win-condition').value
                })
            })
            .then(response => response.json())
            .then(data => {
                symbolSelection.style.display = 'none';
                gameBoard.style.display = 'block';
                document.getElementById('status-message').textContent = `${playerName}'s turn (${playerSymbol})`;
                renderBoard(boardSize);
                startTimer();
                updateAchievements(data.achievements);
                fetchLeaderboard();
                isGameActive = true;
            });
        });
    });

    document.getElementById('board').addEventListener('click', e => {
        if (!isGameActive || !e.target.classList.contains('cell') || e.target.textContent !== '') return;
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        console.log(`Clicked: row=${row}, col=${col}`);
        makeMove(row, col);
    });

    resetButton.addEventListener('click', () => {
        fetch('/reset_game', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            renderBoard(boardSize);
            document.getElementById('status-message').textContent = `${playerName}'s turn (${playerSymbol})`;
            updateScores(data.scores);
            updateAchievements(data.achievements);
            startTimer();
            isGameActive = true;
        });
    });

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLightTheme = document.body.classList.contains('light-theme');
        localStorage.setItem('theme', isLightTheme ? 'light' : 'dark');
    });

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
    }

    themeSelect.addEventListener('change', () => {
        document.getElementById('board').className = `board ${themeSelect.value}-theme`;
    });
});

function renderBoard(size) {
    const board = document.getElementById('board');
    board.innerHTML = '';
    for (let i = 0; i < size; i++) {
        const row = document.createElement('div');
        row.classList.add('row');
        for (let j = 0; j < size; j++) {
            const cell = document.createElement('button');
            cell.classList.add('cell');
            cell.dataset.row = i;
            cell.dataset.col = j;
            row.appendChild(cell);
        }
        board.appendChild(row);
    }
}

function makeMove(row, col) {
    fetch('/make_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col })
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data);
        if (data.winner || data.draw) {
            fetchLeaderboard(); // Update leaderboard when game ends
        }
        resetTimer();
    });
}

function updateBoard(data) {
    const statusMessage = document.getElementById('status-message');
    if (data.board) {
        data.board.forEach((row, i) => {
            row.forEach((value, j) => {
                const cell = document.querySelector(`[data-row="${i}"][data-col="${j}"]`);
                cell.textContent = value;
            });
        });
    }
    if (data.winner) {
        statusMessage.textContent = `${data.winner} wins!`;
        document.getElementById('board').classList.add('winner');
        clearInterval(timer);
        isGameActive = false;
        // Auto-restart after 3 seconds
        setTimeout(() => {
            autoRestartGame();
        }, 3000);
    } else if (data.draw) {
        statusMessage.textContent = "It's a draw!";
        clearInterval(timer);
        isGameActive = false;
        // Auto-restart after 3 seconds
        setTimeout(() => {
            autoRestartGame();
        }, 3000);
    } else if (data.computer_move) {
        setTimeout(() => {
            const cell = document.querySelector(`[data-row="${data.computer_move.row}"][data-col="${data.computer_move.col}"]`);
            cell.textContent = computerSymbol;
            statusMessage.textContent = `${playerName}'s turn (${playerSymbol})`;
        }, 300);
    }
    if (data.event) statusMessage.textContent = data.event;
    updateScores(data.scores || { player: 0, computer: 0 });
    updateAchievements(data.achievements || { hard_wins: 0 });
    if (data.leaderboard) updateLeaderboard(data.leaderboard); // Update leaderboard if included in response
}

function startTimer() {
    clearInterval(timer);
    timeLeft = 10;
    document.getElementById('timer').textContent = `Time: ${timeLeft}s`;
    timer = setInterval(() => {
        timeLeft--;
        document.getElementById('timer').textContent = `Time: ${timeLeft}s`;
        if (timeLeft <= 0) {
            clearInterval(timer);
            // Make a random move for the player if time runs out
            const boardElement = document.getElementById('board');
            const emptyCells = Array.from(document.querySelectorAll('.cell'))
                .filter(cell => cell.textContent === '');
            if (emptyCells.length > 0 && isGameActive) {
                const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
                const row = parseInt(randomCell.dataset.row);
                const col = parseInt(randomCell.dataset.col);
                makeMove(row, col);
            }
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timer);
    startTimer();
}

function updateScores(scores) {
    document.getElementById('player-score').textContent = scores.player;
    document.getElementById('computer-score').textContent = scores.computer;
}

function updateAchievements(achievements) {
    const achDiv = document.getElementById('achievements');
    achDiv.innerHTML = `Achievements: Hard Wins: ${achievements.hard_wins}`;
}

function autoRestartGame() {
    fetch('/reset_game', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById('board').classList.remove('winner');
        renderBoard(boardSize);
        document.getElementById('status-message').textContent = `${playerName}'s turn (${playerSymbol})`;
        updateScores(data.scores);
        updateAchievements(data.achievements);
        startTimer();
        isGameActive = true;
    });
}

function updateLeaderboard(leaderboard) {
    const lbDiv = document.getElementById('leaderboard');
    lbDiv.innerHTML = '<h3>Leaderboard</h3>' + Object.entries(leaderboard)
        .map(([name, stats]) => `${name}: ${stats.wins} wins, ${stats.games} games`)
        .join('<br>');
}

function fetchLeaderboard() {
    fetch('/leaderboard')
        .then(response => response.json())
        .then(data => updateLeaderboard(data));
}