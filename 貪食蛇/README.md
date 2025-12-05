以下說明會用**易於教學的方式**，完整解析這支 Pygame 貪食蛇程式，並整理「你可以手動調整的參數」。
（全程使用繁體中文）

---

# 🟩 程式整體架構說明

這份程式由以下幾大部分組成：

1. **環境初始化（pygame.init()）**
2. **全域參數設定（視窗大小、顏色、速度等）**
3. **Snake 類別：處理蛇的身體、移動、方向、碰撞與繪製**
4. **Food 類別：處理食物生成與顯示**
5. **一些 UI 畫面繪製函式（網格、分數、開始畫面、結束畫面）**
6. **main() 主迴圈：處理遊戲狀態（start / playing / game_over）**

---

# 🟦 程式詳細解說（逐段講解）

## 🔹 初始化與基本設定

```python
pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
```

這裡設定遊戲視窗大小 600×600，每格為 20×20，因此產生 30×30 的格子。

---

## 🔹 顏色設定

```python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)
GRAY = (40, 40, 40)
```

之後畫蛇、食物、網格會用到。

---

## 🔹 遊戲速度控制

```python
START_FPS = 5
MAX_FPS = 15

def get_speed(score):
    speed = START_FPS + (score // 30)
    return min(speed, MAX_FPS)
```

分數每 30 分加速一次（蛇吃一次 +10 分）。

---

## 🔹 初始化視窗 & 字型

```python
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("貪食蛇遊戲")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
```

---

# 🟧 Snake 類別

負責：

* 初始位置
* 移動
* 長大
* 方向改變
* 自己撞自己
* 撞牆
* 繪製到畫面

### 初始化與 reset()

```python
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
```

蛇從畫面中心開始，向右移動。

---

### 移動

```python
def move(self):
    head_x, head_y = self.body[0]
    dir_x, dir_y = self.direction
    new_head = (head_x + dir_x, head_y + dir_y)

    self.body.insert(0, new_head)

    if not self.grow:
        self.body.pop()
    else:
        self.grow = False
```

* 插入新頭
* 若沒有吃到食物 → 刪除尾巴
* 吃到食物 → `grow=True`，讓蛇變長

---

### 方向變換（避免反向）

```python
def change_direction(self, new_direction):
    opposite = (-self.direction[0], -self.direction[1])
    if new_direction != opposite:
        self.direction = new_direction
```

不能直接反方向（避免 180 度轉身自殺）。

---

### 碰撞檢查

```python
def check_collision(self):
    head = self.body[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH:
        return True
    if head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    if head in self.body[1:]:
        return True
    return False
```

判斷：

* 撞牆
* 撞到自己

---

### Snake.draw：繪製蛇

---

# 🟥 Food 類別

```python
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
```

### 隨機生成食物

```python
def spawn(self, snake_body=None):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)
        if snake_body is None or self.position not in snake_body:
            break
```

確保食物不會生成在蛇身上。

---

# 🟦 介面繪製（開始畫面、網格、分數、結束畫面）

都只是用字型、矩形、顏色把 UI 畫到畫布上。

---

# 🟩 main() 主迴圈

核心：

* 接收鍵盤事件
* 控制遊戲狀態（start / playing / game_over）
* 更新蛇的位置
* 檢查碰撞
* 吃食物
* 畫整個畫面
* 控制 FPS

---

# 🟪 你可以手動調整的參數清單（最重要）

以下是**玩家常會調的數值**，全部整理如下：

## 🎮 1. 視窗大小

```python
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
```

改成 800×800、1000×600 都可以。

---

## 📏 2. 格子大小（蛇的大小）

```python
GRID_SIZE = 20
```

* 越大 → 蛇變粗、格子變少
* 越小 → 蛇變細、格子變多（難度提升）

---

## 🎨 3. 顏色（自行定義）

例如：

```python
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
```

---

## 🕒 4. 遊戲速度（FPS）

```python
START_FPS = 5
MAX_FPS = 15
```

你可改成：

```python
START_FPS = 10  # 開始更快
MAX_FPS = 25    # 最高速度更快
```

---

## ➕ 5. 每吃一個加幾分

```python
score += 10
```

改成：

```python
score += 1
```

或：

```python
score += 50
```

---

## 🍎 6. 食物外框 / 大小

```python
rect = pygame.Rect(x, y, GRID_SIZE - 2, GRID_SIZE - 2)
```

改成 `GRID_SIZE` 就會把格子填滿。

---

## 🐍 7. 蛇（頭、身體）顏色

```python
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
```

也能新增彩虹蛇、gradient 等效果。

---

## 🎯 8. 增加新的遊戲規則

你可以手動增加：

* 蛇加速方式
* 兩個食物同時出現
* 障礙物
* 邊界穿越（撞牆不死）

但這部分屬於「程式修改」，不是簡單參數。

---

# 🟦 如果你需要，我可以做更多：

✔ 提供精簡版教學用程式
✔ 幫你做更漂亮的 UI
✔ 添加背景音樂
✔ 加入排行榜、暫停、無敵模式
✔ 改成物件導向教案版本
✔ 變成可輸出 EXE

只要告訴我你要哪種！

---

如果你願意，我可以幫你整理成「學生用講義」或「逐步拆解教學版」。
