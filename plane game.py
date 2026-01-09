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

