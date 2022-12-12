import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class ShooterGame extends JFrame {
  // game loop variables
  private int frameCount;
  private long startTime;
  private long elapsedTime;
  private long prevTime;
  private long currTime;
  private long fps;
  private double delta;

  // game state variables
  private boolean gameRunning;
  private int score;

  // player variables
  private int playerX;
  private int playerY;
  private int playerSpeed;

  // enemy variables
  private int enemyX;
  private int enemyY;
  private int enemySpeed;

  // constructor
  public ShooterGame() {
    super("2D Shooter Game");
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    // initialize game loop variables
    frameCount = 0;
    startTime = System.nanoTime();
    prevTime = startTime;

    // initialize game state variables
    gameRunning = true;
    score = 0;

    // initialize player variables
    playerX = 0;
    playerY = 0;
    playerSpeed = 10;

    // initialize enemy variables
    enemyX = 100;
    enemyY = 100;
    enemySpeed = 5;

    // create game panel and add it to the frame
    GamePanel gamePanel = new GamePanel();
    add(gamePanel);
    pack();
    setVisible(true);
  }

  // main game loop
  private void gameLoop() {
    // update game state
    if (gameRunning) {
      // update player position
      
    }
  }
}