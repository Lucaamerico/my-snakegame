<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Snake Game</title>
  <style>
    canvas {
      background-color: black;
      display: block;
      margin: 0 auto;
      border: 2px solid #333;
    }
    body {
      font-family: monospace;
      text-align: center;
      color: white;
      background-color: #111;
    }
  </style>
</head>
<body>
  <h1>Snake Game</h1>
  <p>Use Arrow Keys to Control the Snake</p>
  <canvas id="gameCanvas" width="400" height="400"></canvas>
  <p id="score">Score: 0</p>
  <p id="gameOver" style="display: none;">Game Over! Press R to restart.</p>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    const tileSize = 20;
    const tileCount = canvas.width / tileSize;
    let snake = [ { x: 10, y: 10 } ];
    let food = { x: 5, y: 5 };
    let velocity = { x: 1, y: 0 };
    let score = 0;
    let gameOver = false;

    function drawRect(x, y, color) {
      ctx.fillStyle = color;
      ctx.fillRect(x * tileSize, y * tileSize, tileSize, tileSize);
    }

    function drawGame() {
      if (gameOver) return;

      update();
      draw();
      setTimeout(drawGame, 100);
    }

    function update() {
      const head = { x: snake[0].x + velocity.x, y: snake[0].y + velocity.y };

      // Check for wall collision
      if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        return endGame();
      }

      // Check for self collision
      for (let segment of snake) {
        if (segment.x === head.x && segment.y === head.y) {
          return endGame();
        }
      }

      snake.unshift(head);

      // Check for food
      if (head.x === food.x && head.y === food.y) {
        score++;
        document.getElementById('score').textContent = 'Score: ' + score;
        placeFood();
      } else {
        snake.pop();
      }
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawRect(food.x, food.y, 'red');
      snake.forEach((segment, index) => drawRect(segment.x, segment.y, index === 0 ? 'green' : 'lime'));
    }

    function placeFood() {
      food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
      };

      // Avoid placing food on the snake
      for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
          return placeFood();
        }
      }
    }

    function endGame() {
      gameOver = true;
      document.getElementById('gameOver').style.display = 'block';
    }

    document.addEventListener('keydown', e => {
      if (gameOver && e.key.toLowerCase() === 'r') {
        // Restart the game
        snake = [ { x: 10, y: 10 } ];
        velocity = { x: 1, y: 0 };
        score = 0;
        document.getElementById('score').textContent = 'Score: 0';
        document.getElementById('gameOver').style.display = 'none';
        gameOver = false;
        placeFood();
        drawGame();
      }

      if (e.key === 'ArrowUp' && velocity.y === 0) {
        velocity = { x: 0, y: -1 };
      } else if (e.key === 'ArrowDown' && velocity.y === 0) {
        velocity = { x: 0, y: 1 };
      } else if (e.key === 'ArrowLeft' && velocity.x === 0) {
        velocity = { x: -1, y: 0 };
      } else if (e.key === 'ArrowRight' && velocity.x === 0) {
        velocity = { x: 1, y: 0 };
      }
    });

    drawGame();
  </script>
</body>
</html>
