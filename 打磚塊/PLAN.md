# 打磚塊遊戲（Breakout Game）開發計畫書

## 1. 專案目標（Project Goal）

使用 Python 與 pygame 製作一個經典的「打磚塊」遊戲，  
專案設計重點為 **可讀性、可修改性、教學友善**，  
讓初學者可以透過修改「常數設定」快速調整遊戲行為。

---

## 2. 使用技術（Tech Stack）

- 語言：Python 3.x
- 遊戲函式庫：pygame
- 架構風格：
  - 單一主程式（`main.py`）
  - 以「常數設定區」集中管理遊戲參數
  - 使用 class 表示遊戲物件（Ball / Paddle / Brick）

---

## 3. 遊戲玩法說明（Gameplay）

- 玩家使用滑鼠或鍵盤左右移動擋板（Paddle）
- 球（Ball）會反彈牆壁、擋板與磚塊
- 球碰到磚塊時：
  - 磚塊消失
  - 玩家得分
- 球掉落畫面底部：
  - 扣一條命
  - 球與擋板重置
- 磚塊全部消失：
  - 顯示「勝利畫面」
- 生命歸零：
  - 顯示「遊戲結束」

---

## 4. 可調整常數設計（非常重要）

### 4.1 視窗設定

```python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
```


### 4.2顏色設定
```python
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
GREEN = (0, 255, 0)
```

### 4.3 擋板（Paddle）設定
```python
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
PADDLE_Y_OFFSET = 40   # 距離畫面底部的高度
```

### 4.4 球（Ball）設定
```python
BALL_RADIUS = 8
BALL_SPEED_X = 5
BALL_SPEED_Y = -5
```

### 4.5 磚塊（Brick）設定
```pytnon
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_PADDING = 5
BRICK_TOP_OFFSET = 60
```

### 4.6 遊戲規則設定
```python
PLAYER_LIVES = 3
SCORE_PER_BRICK = 10
```

## 5. 遊戲物件設計（Class Design）

### 5.1 Paddle 類別
職責：

儲存位置與大小

處理左右移動

繪製自己

```python
Paddle
- x, y
- width, height
- speed
- move_left()
- move_right()
- draw()

```

### 5.2 Ball 類別
職責：

儲存位置、速度

移動與反彈邏輯

碰撞判斷（牆壁 / 擋板 / 磚塊）

```python
Ball
- x, y
- speed_x, speed_y
- move()
- bounce_x()
- bounce_y()
- reset()
- draw()


```

### 5.3 Brick 類別
職責：

儲存位置與是否存在

被擊中後消失

```python
Brick
- rect
- alive
- draw()

```

## 6. 遊戲流程（Main Loop)

```python
初始化 pygame
建立 Paddle / Ball / Bricks
while 遊戲進行中:
    處理事件（鍵盤 / 滑鼠 / 離開）
    更新遊戲狀態
    碰撞判斷
    繪製畫面
    控制 FPS

```

## 7. 顯示資訊（HUD）

左上角顯示：

分數（Score）

剩餘生命（Lives）

## 8. 結束畫面

勝利畫面：

顯示「YOU WIN」

失敗畫面：

顯示「GAME OVER」

提示玩家：

按任意鍵重新開始

或 ESC 離開


