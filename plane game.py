第一段：匯入套件 + 常數與顏色設定
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
第二段：PlaneGame 類別 + 遊戲資料初始化
class PlaneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("尋找機頭 - 隨機變體版")
        
        # 遊戲數據
        self.grid_data = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.planes = []
        self.total_heads = 0
        self.found_heads = 0
        self.steps = 0
        self.game_over = False
#第三段：上方資訊列 UI
                # --- 介面佈局 ---
        self.top_frame = tk.Frame(root, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.lbl_steps = tk.Label(self.top_frame, text="步數: 0", font=("Arial", 12))
        self.lbl_steps.pack(side=tk.LEFT, padx=20)
        
        self.lbl_heads = tk.Label(
            self.top_frame, text="剩餘機頭: 0",
            font=("Arial", 12, "bold"), fg="red"
        )
        self.lbl_heads.pack(side=tk.LEFT, padx=20)
        
        self.btn_restart = tk.Button(
            self.top_frame, text="重新開始", command=self.ask_start_game
        )
        self.btn_restart.pack(side=tk.RIGHT, padx=20)
#第四段：主容器 + 遊戲盤 Grid
        self.main_container = tk.Frame(root)
        self.main_container.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.game_frame = tk.Frame(self.main_container)
        self.game_frame.pack(side=tk.LEFT, padx=10)
        
        self._init_grid_ui()

    def _init_grid_ui(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.game_frame,
                    width=4, height=2,
                    bg=COLOR_DEFAULT,
                    command=lambda row=r, col=c: self.on_click(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn
#第五段：右側提示區（Canvas）
        self.info_frame = tk.Frame(self.main_container, width=200)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.lbl_info_title = tk.Label(
            self.info_frame, text="本局敵機情報", font=("Arial", 11, "bold")
        )
        self.lbl_info_title.pack(pady=5)
        
        self.preview_canvas = tk.Canvas(
            self.info_frame, width=150, height=400, bg="#F0F0F0"
        )
        self.preview_canvas.pack(expand=True, fill=tk.BOTH)

        self.ask_start_game()

