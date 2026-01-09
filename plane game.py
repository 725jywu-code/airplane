import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# --- 1. 常數設定 ---
GRID_SIZE = 10
CELL_SIZE = 40        # 遊戲格大小
PREVIEW_CELL_SIZE = 20  # 右側預覽格大小

# --- 2. 顏色定義 ---
COLOR_DEFAULT = "#DDDDDD" # 未翻開的顏色 (灰色)
COLOR_MISS = "white"      # 沒打中 (白色)
COLOR_BODY = "#5555FF"    # 機身 (藍色)
COLOR_HEAD = "#FF4444"    # 機頭 (紅色)
COLOR_TEXT = "black"

# --- 3. 主遊戲類別 ---
class PlaneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("尋找機頭 - 隨機變體版")
        
        # 遊戲數據初始化
        self.grid_data = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.planes = []
        self.total_heads = 0
        self.found_heads = 0
        self.steps = 0
        self.game_over = False

        # 介面佈局設置
        self._setup_ui()
        
        # 啟動遊戲
        self.ask_start_game()

    # --- A. 介面初始化方法 (UI Setup) ---
    
    def _setup_ui(self):
        """設置遊戲介面的頂部資訊列、遊戲盤和右側提示區。"""
        # 1. 頂部資訊列 (步數, 剩餘機頭, 重新開始按鈕)
        self.top_frame = tk.Frame(self.root, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.lbl_steps = tk.Label(self.top_frame, text="步數: 0", font=("Arial", 12))
        self.lbl_steps.pack(side=tk.LEFT, padx=20)
        
        self.lbl_heads = tk.Label(self.top_frame, text="剩餘機頭: 0", font=("Arial", 12, "bold"), fg="red")
        self.lbl_heads.pack(side=tk.LEFT, padx=20)
        
        self.btn_restart = tk.Button(self.top_frame, text="重新開始", command=self.ask_start_game)
        self.btn_restart.pack(side=tk.RIGHT, padx=20)

        # 下方主容器 (容納遊戲盤和提示區)
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # 2. 左側遊戲盤 Grid
        self.game_frame = tk.Frame(self.main_container)
        self.game_frame.pack(side=tk.LEFT, padx=10)
        self._init_grid_ui()

        # 3. 右側提示區 (顯示飛機形狀)
        self.info_frame = tk.Frame(self.main_container, width=200)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        self.lbl_info_title = tk.Label(self.info_frame, text="本局敵機情報", font=("Arial", 11, "bold"))
        self.lbl_info_title.pack(pady=5)
        
        self.preview_canvas = tk.Canvas(self.info_frame, width=150, height=400, bg="#F0F0F0")
        self.preview_canvas.pack(expand=True, fill=tk.BOTH)

    def _init_grid_ui(self):
        """初始化 10x10 的按鈕網格"""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                btn = tk.Button(self.game_frame, width=4, height=2, bg=COLOR_DEFAULT,
                                command=lambda row=r, col=c: self.on_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

    # --- B. 遊戲控制方法 (Game Control) ---

    def ask_start_game(self):
        """詢問玩家要幾架飛機，並開始遊戲。"""
        # 優化 try/except 塊，僅依賴 simpledialog 的返回值
        num = simpledialog.askinteger("遊戲設定", "請輸入飛機數量 (2 或 3):", 
                                      minvalue=2, maxvalue=3, parent=self.root)
            
        if num is None: 
            # 如果是第一次啟動遊戲，且使用者按取消，則退出應用程式
            if self.steps == 0 and self.total_heads == 0: 
                 self.root.quit()
            return # 使用者按取消
            
        self.start_game(num)

    def start_game(self, num_planes):
        """重置所有數據並開始新遊戲。"""
        self.game_over = False
        self.steps = 0
        self.total_heads = num_planes
        self.found_heads = 0
        self.planes = []
        
        # 重置 UI 狀態
        self.lbl_steps.config(text="步數: 0")
        self.update_head_label()
        self.preview_canvas.delete("all")
        
        # 重置盤面數據和按鈕狀態
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.grid_data[r][c] = None
                self.buttons[r][c].config(bg=COLOR_DEFAULT, state=tk.NORMAL, text="")

        # 生成並放置飛機
        self.place_planes(num_planes)
        
        # 繪製右側提示
        self.draw_plane_previews()

    def update_head_label(self):
        """更新剩餘機頭的標籤顯示。"""
        remain = self.total_heads - self.found_heads
        self.lbl_heads.config(text=f"剩餘機頭: {remain}")

    def check_win(self):
        """檢查是否滿足獲勝條件。"""
        if self.found_heads == self.total_heads:
            self.game_over = True
            messagebox.showinfo("獲勝！", f"恭喜！你用了 {self.steps} 步找到了所有飛機！")

    # --- C. 遊戲互動/點擊處理方法 (Interaction) ---

    def on_click(self, r, c):
        """處理點擊事件，判斷是否命中。"""
        if self.game_over: return
        
        btn = self.buttons[r][c]
        if btn['state'] == tk.DISABLED: return # 已經點過了

        self.steps += 1
        self.lbl_steps.config(text=f"步數: {self.steps}")
        
        content = self.grid_data[r][c]
        
        btn.config(state=tk.DISABLED) # 點擊後禁用按鈕
        
        if content is None:
            # 空白 (白色)
            btn.config(bg=COLOR_MISS)
        elif content == 'B':
            # 機身 (藍色)
            btn.config(bg=COLOR_BODY)
        elif content == 'H':
            # 機頭 (紅色)
            btn.config(bg=COLOR_HEAD, text="X")
            self.found_heads += 1
            self.update_head_label()
            self.check_win()

    # --- D. 飛機生成與放置方法 (Plane Generation) ---

    def generate_random_shape(self):
        """
        隨機生成飛機形狀。
        回傳一個 list of tuples [(x, y), ... ]，相對座標，(0,0) 為機頭。
        """
        # 基礎結構：機頭(0,0)，機身頸部(0,1)
        shape = [(0, 0), (0, 1)]
        
        wing_y = 1
        wing_len = random.randint(1, 3) # 機翼長度 1~3
        body_len = random.randint(2, 4) # 機身總長 2~4
        
        # 建立機身
        for i in range(2, body_len + 1):
            shape.append((0, i))
            
        # 建立機翼 (在 wing_y 的位置左右延伸)
        for i in range(1, wing_len + 1):
            shape.append((-i, wing_y)) # 左翼
            shape.append((i, wing_y))  # 右翼
            
        # 偶爾加個機尾翼 (50% 機率)
        if random.choice([True, False]):
            tail_y = body_len
            shape.append((-1, tail_y))
            shape.append((1, tail_y))
            
        return shape

    def rotate_shape(self, shape, angle):
        """根據角度旋轉座標點。"""
        new_shape = []
        for x, y in shape:
            if angle == 0: nx, ny = x, y
            elif angle == 90: nx, ny = -y, x
            elif angle == 180: nx, ny = -x, -y
            elif angle == 270: nx, ny = y, -x
            new_shape.append((nx, ny))
        return new_shape

    def is_valid_position(self, r, c, shape):
        """檢查該位置是否可以放置飛機（不越界、不重疊）。"""
        for dx, dy in shape:
            # 注意：grid 是 [row][col], row對應y, col對應x
            nr, nc = r + dy, c + dx
            if not (0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE):
                return False # 越界
            if self.grid_data[nr][nc] is not None:
                return False # 重疊
        return True

    def add_plane_to_grid(self, r, c, shape):
        """將飛機數據寫入 grid_data。"""
        for i, (dx, dy) in enumerate(shape):
            nr, nc = r + dy, c + dx
            # 索引 0 是機頭
            if i == 0:
                self.grid_data[nr][nc] = 'H'
            else:
                self.grid_data[nr][nc] = 'B'

    def place_planes(self, count):
        """嘗試在盤面上放置指定數量的飛機。"""
        placed_count = 0
        attempts = 0
        
        while placed_count < count and attempts < 1000:
            attempts += 1
            raw_shape = self.generate_random_shape()
            rotation = random.choice([0, 90, 180, 270])
            rotated_shape = self.rotate_shape(raw_shape, rotation)
            
            # 隨機位置
            start_r = random.randint(0, GRID_SIZE-1)
            start_c = random.randint(0, GRID_SIZE-1)
            
            if self.is_valid_position(start_r, start_c, rotated_shape):
                self.add_plane_to_grid(start_r, start_c, rotated_shape)
                self.planes.append(raw_shape)  # 記錄原始形狀供右側顯示
                placed_count += 1

    # --- E. 繪圖方法 (Drawing) ---
    
    def draw_plane_previews(self):
        """在右側 Canvas 畫出這局生成的飛機樣子。"""
        y_offset = 20
        x_center = 75
        
        for idx, shape in enumerate(self.planes):
            # 標題
            self.preview_canvas.create_text(x_center, y_offset, text=f"飛機 {idx+1}", font=("Arial", 10))
            y_offset += 20
            
            # 找形狀的邊界以計算置中
            ys = [p[1] for p in shape]
            
            # 繪製每一個格子
            for i, (dx, dy) in enumerate(shape):
                # 轉換座標到 canvas (小格子)
                # dy 是相對機頭的垂直偏移，+20 是為了在 canvas 中將機頭往下拉，顯示完整
                cx = x_center + dx * PREVIEW_CELL_SIZE
                cy = y_offset + dy * PREVIEW_CELL_SIZE + 20
                
                color = COLOR_HEAD if i == 0 else COLOR_BODY
                self.preview_canvas.create_rectangle(
                    cx - PREVIEW_CELL_SIZE/2, cy - PREVIEW_CELL_SIZE/2,
                    cx + PREVIEW_CELL_SIZE/2, cy + PREVIEW_CELL_SIZE/2,
                    fill=color, outline="white"
                )
            
            # 計算下一個圖形的偏移量 (根據飛機高度)
            height_blocks = max(ys) - min(ys) + 1
            y_offset += (height_blocks * PREVIEW_CELL_SIZE) + 40

# --- 4. 程式進入點 ---

if __name__ == "__main__":
    root = tk.Tk()
    # 設定視窗大小與位置
    root.geometry("600x550")
    game = PlaneGame(root)
    root.mainloop()