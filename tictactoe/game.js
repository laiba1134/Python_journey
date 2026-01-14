// Game state
let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameMode = ""; // "ai" or "pvp"
let gameActive = true;
let matchesToPlay = 3;
let currentMatch = 1;
let roundsPlayed = 0;  
let player1Wins = 0;
let player2Wins = 0;
let selectedMode = null;
// Get elements
const menuScreen = document.getElementById("menu-screen");
const gameScreen = document.getElementById("game-screen");
const aiModeBtn = document.getElementById("ai-mode");
const pvpModeBtn = document.getElementById("pvp-mode");
const startBtn = document.getElementById("start-btn");
const cells = document.querySelectorAll(".cell");
const resetBtn = document.getElementById("reset-btn");
const player1Score = document.getElementById("player1-score");
const player2Score = document.getElementById("player2-score");
const matchBtns = document.querySelectorAll(".match-btn");

// Mode selection (don't start game yet, just select mode)
aiModeBtn.addEventListener("click", () => {
    selectedMode = "ai";
    aiModeBtn.classList.add("active");
    pvpModeBtn.classList.remove("active");
});

pvpModeBtn.addEventListener("click", () => {
    selectedMode = "pvp";
    pvpModeBtn.classList.add("active");
    aiModeBtn.classList.remove("active");
});

// Match selection
matchBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        matchBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        matchesToPlay = parseInt(btn.dataset.matches);
    });
});

// Start game button
startBtn.addEventListener("click", () => {
    if (!selectedMode) {
        alert("Please select a game mode!");
        return;
    }
    gameMode = selectedMode;
    
    // Randomize starting player
    currentPlayer = Math.random() < 0.5 ? "X" : "O";
    
    menuScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
    updateScoreDisplay();
    updateTurnIndicator();
    updateStatusMessage();
    
    // If AI starts, make the first move
    if (gameMode === "ai" && currentPlayer === "O") {
        setTimeout(aiMove, 500);
    }
});

// Cell click handler
cells.forEach(cell => {
    cell.addEventListener("click", handleCellClick);
});

// Handle cell click
function handleCellClick(e) {
    const index = parseInt(e.target.dataset.index);
    
    if (board[index] !== "" || !gameActive) return;
    
    makeMove(index, currentPlayer);
    
    if (checkWinner(currentPlayer)) {
    if (currentPlayer === "X") {
        player1Wins++;
    } else {
        player2Wins++;
    }
    roundsPlayed++;  // ADD THIS
    updateScoreDisplay();
    
    if (isMatchOver()) {
        showFinalWinner();
    } else {
        updateStatusMessage(`${getCurrentPlayerName()} wins this round!`);
        setTimeout(nextRound, 1500);
    }
    return;
}

if (checkDraw()) {
    roundsPlayed++;  
    if (isMatchOver()) {
        showFinalWinner();
    } else {
        updateStatusMessage("It's a draw!");
        setTimeout(nextRound, 1500);
    }
    return;
}
    
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    updateTurnIndicator();
    updateStatusMessage();
    
    // AI move
    if (gameMode === "ai" && currentPlayer === "O" && gameActive) {
        setTimeout(aiMove, 500);
    }
}

// Make move
function makeMove(index, player) {
    board[index] = player;
    cells[index].textContent = player;
    cells[index].classList.add(player.toLowerCase());
}

// Get current player name
function getCurrentPlayerName() {
    if (currentPlayer === "X") {
        return "Player 1";
    } else {
        return gameMode === "ai" ? "AI" : "Player 2";
    }
}

// Update status message
function updateStatusMessage(message = null) {
    const statusMsg = document.getElementById("status-message");
    if (statusMsg) {
        if (message) {
            statusMsg.textContent = message;
        } else {
            statusMsg.textContent = `${getCurrentPlayerName()}'s turn`;
        }
    }
}

// Update turn indicator (glowing effect)
function updateTurnIndicator() {
    if (currentPlayer === "X") {
        player1Score.classList.add("active");
        player2Score.classList.remove("active");
    } else {
        player2Score.classList.add("active");
        player1Score.classList.remove("active");
    }
}

// Update score display
function updateScoreDisplay() {
    const p1ScoreEl = player1Score.querySelector(".score-number");
    const p2ScoreEl = player2Score.querySelector(".score-number");
    p1ScoreEl.textContent = player1Wins;
    p2ScoreEl.textContent = player2Wins;
}

// Check if match is over
// Check if match is over
function isMatchOver() {
    return roundsPlayed >= matchesToPlay;
}
// Show final winner
function showFinalWinner() {
    gameActive = false;
    
    const gameBoard = document.getElementById("game-board");
    const statusBar = document.getElementById("status-bar");
    
    // Create winner announcement
    const winnerDiv = document.createElement("div");
    winnerDiv.className = "winner-announcement";
    winnerDiv.id = "winner-announcement";
    
    let winnerText = "";
    if (player1Wins > player2Wins) {
        winnerText = `
            <h2> PLAYER 1 WINS! </h2>
            <p>Final Score: ${player1Wins} - ${player2Wins}</p>
        `;
    } else if (player2Wins > player1Wins) {
        const player2Name = gameMode === "ai" ? "AI" : "PLAYER 2";
        winnerText = `
            <h2> ${player2Name} WINS! </h2>
            <p>Final Score: ${player1Wins} - ${player2Wins}</p>
        `;
    } else {
        winnerText = `
            <h2> IT'S A TIE! </h2>
            <p>Final Score: ${player1Wins} - ${player2Wins}</p>
        `;
    }
    
    winnerDiv.innerHTML = winnerText;
    
    // Insert winner announcement
    gameBoard.parentNode.insertBefore(winnerDiv, gameBoard);
    if (statusBar) statusBar.style.display = "none";
}

// Next round
function nextRound() {
    currentMatch++;
    board = ["", "", "", "", "", "", "", "", ""];
    gameActive = true;
    
    // Randomize starting player for each round
    currentPlayer = Math.random() < 0.5 ? "X" : "O";
    
    cells.forEach(cell => {
        cell.textContent = "";
        cell.classList.remove("x", "o");
    });
    
    updateTurnIndicator();
    updateStatusMessage();
    
    // If AI starts this round, make the first move
    if (gameMode === "ai" && currentPlayer === "O") {
        setTimeout(aiMove, 500);
    }
}

// Back to // Back to menu
function backToMenu() {
    // Remove winner announcement if it exists
    const winnerAnnouncement = document.getElementById("winner-announcement");
    if (winnerAnnouncement) {
        winnerAnnouncement.remove();
    }
    
    // Show status bar again
    const statusBar = document.getElementById("status-bar");
    if (statusBar) statusBar.style.display = "block";
    
    gameScreen.classList.add("hidden");
    menuScreen.classList.remove("hidden");
    
    // Reset everything
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameActive = true;
    player1Wins = 0;
    player2Wins = 0;
    currentMatch = 1;
    roundsPlayed = 0;  
    
    cells.forEach(cell => {
        cell.textContent = "";
        cell.classList.remove("x", "o");
    });
}

// Check winner
function checkWinner(player) {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
        [0, 4, 8], [2, 4, 6] // diagonals
    ];
    
    return winPatterns.some(pattern => {
        const [a, b, c] = pattern;
        return board[a] && board[a] === board[b] && board[a] === board[c];
    });
}

// Check draw
function checkDraw() {
    return board.every(cell => cell !== "");
}

// Smart AI move (from your Python code)
function aiMove() {
    const aiPlayer = "O";
    const userPlayer = "X";
    
    // 1. Can AI win this move?
    for (let i = 0; i < 9; i++) {
        if (board[i] === "") {
            board[i] = aiPlayer;
            if (checkWinner(aiPlayer)) {
                makeMove(i, aiPlayer);
                checkGameEnd();
                return;
            }
            board[i] = "";
        }
    }
    
    // 2. Can player win next move? Block it
    for (let i = 0; i < 9; i++) {
        if (board[i] === "") {
            board[i] = userPlayer;
            if (checkWinner(userPlayer)) {
                board[i] = "";
                makeMove(i, aiPlayer);
                checkGameEnd();
                return;
            }
            board[i] = "";
        }
    }
    
    // 3. Pick center if free
    if (board[4] === "") {
        makeMove(4, aiPlayer);
        checkGameEnd();
        return;
    }
    
    // 4. Pick a corner if free
    const corners = [0, 2, 6, 8];
    for (let i of corners) {
        if (board[i] === "") {
            makeMove(i, aiPlayer);
            checkGameEnd();
            return;
        }
    }
}
    // 5. Pick any remaining cell
    const emptyCells = board.map((cell, index) => cell === "" ? index : null).filter(i => i !== null);
    const randomIndex = emptyCells[Math.floor(Math.random() * emptyCells.length)];
    makeMove(randomIndex, aiPlayer);
    checkGameEnd();
// Check game end after AI move
function checkGameEnd() {
    if (checkWinner("O")) {
        player2Wins++;
        roundsPlayed++;  // ADD THIS
        updateScoreDisplay();
        
        if (isMatchOver()) {
            showFinalWinner();
        } else {
            updateStatusMessage("AI wins this round!");
            setTimeout(nextRound, 1500);
        }
        return;
    }
    
    if (checkDraw()) {
        roundsPlayed++; 
        if (isMatchOver()) {
            showFinalWinner();
        } else {
            updateStatusMessage("It's a draw!");
            setTimeout(nextRound, 1500);
        }
        return;
    }
    
    currentPlayer = "X";
    updateTurnIndicator();
    updateStatusMessage();
}
// Reset button
resetBtn.addEventListener("click", backToMenu);