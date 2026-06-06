#!/usr/bin/env python
# coding: utf-8

# ============================================================
# 学生用メニュー   id: stu_menu.py
# ------------------------------------------------------------
# 役割: 学生がデスクトップから起動するトップ画面。
#       検索 / 費用推定 / 終了 の3ボタンを持ち、
#       検索ボタン  → search_1.py    を subprocess で起動
#       推定ボタン  → ai_estim_2.py  を subprocess で起動
#
# 設計判断:
#   - 親子起動の構造は jyugyo_subprocess.ipynb の親(tst_oya.py)を踏襲
#   - subprocess.run() は子プログラム終了まで待つ → 学生用メニューに自然に戻る
#   - 画面デザインは「標準画面サンプル_2.png」(職員用メニュー) に準じる
#       緑タイトル / 水色グループ枠 / 下部ピンクのメッセージエリア / 黄色の終了ボタン
# ============================================================

import tkinter as tk
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox as tkMB

APP_DIR = Path(__file__).resolve().parent

# ---------- 子プログラム起動の共通関数 -------------------------
def run_child(child_py: str, btn_label: str):
    child_path = APP_DIR / child_py
    if not child_path.exists():
        msg_area.configure(text=f"{child_py} が見つかりません")
        return

    msg_area.configure(text=f"{btn_label} 起動中...")
    root.update()

    try:
        res = subprocess.run(
            [sys.executable, str(child_path)],
            cwd=APP_DIR,
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            msg_area.configure(text=f"{btn_label} 正常終了")
        else:
            msg_area.configure(text=f"{btn_label} 異常終了")
    except Exception as e:
        msg_area.configure(text=f"起動エラー: {e}")


def go_search():
    run_child("search_1.py", "検索")

def go_estim():
    run_child("ai_estim_2.py", "費用推定")

def go_owari():
    if tkMB.askyesno("確認", "終了しますか？"):
        root.destroy()


# ============================================================
# 画面構築
# ============================================================
root = tk.Tk()
root.title("賃貸情報管理MENU(学生用)")
root.geometry("700x500")
root.configure(bg="white")

# ---------- タイトル (緑バー) ---------------------------------
title = tk.Label(
    root,
    text="  賃貸情報提供システム学生用メニュー  ",
    fg="light green", bg="dark green",
    font=("Helvetica", 20, "bold italic")
)
title.place(x=80, y=20)

# ---------- 機能ボタンエリア (水色グループ枠) -----------------
# 設計判断: LabelFrame はラベル部分が親の背景色を引き継いで
#           はみ出して見える問題があるため Frame+Label で代替。
BG_BLUE = "#87CEFA"

frame_outer = tk.Frame(root, bg=BG_BLUE, bd=2, relief=tk.GROOVE)
frame_outer.place(x=190, y=110, width=320, height=220)

tk.Label(
    frame_outer, text=" 物件情報を調べる ",
    bg=BG_BLUE, fg="black",
    font=("", 12, "bold")
).pack(anchor="w", padx=8, pady=(6, 0))

frame_inner = tk.Frame(frame_outer, bg=BG_BLUE)
frame_inner.pack(expand=True)

btn_search = tk.Button(
    frame_inner, text="検 索",
    width=14, height=1,
    font=("", 14, "bold"),
    command=go_search
)
btn_search.pack(pady=10)

btn_estim = tk.Button(
    frame_inner, text="費用推定",
    width=14, height=1,
    font=("", 14, "bold"),
    command=go_estim
)
btn_estim.pack(pady=5)

# ---------- メッセージエリア (ピンクの帯) ---------------------
msg_area = tk.Label(
    root,
    text=" ",
    bg="pink",
    width=40, height=3,
    relief=tk.SUNKEN,
    font=("", 14)
)
msg_area.place(x=60, y=380)

# ---------- 終了ボタン (黄色) ---------------------------------
btn_owari = tk.Button(
    root, text="終 了",
    bg="yellow2", fg="red",
    width=8, height=2,
    font=("", 14, "bold italic"),
    command=go_owari
)
btn_owari.place(x=560, y=390)

root.mainloop()
