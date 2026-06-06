#!/usr/bin/env python
# coding: utf-8

# Menu 画面
# Yachin_menu.py
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox as tkMB

APP_DIR = Path(__file__).resolve().parent



Master_tbl = [("地区コード", 1),("月額費用クラス", 2)]
bukken_tbl = [("テーブルロード", 1),("個別追加処理", 2),("一括追加処理", 3),("データ検索・変更", 4),("　予備　", 5)]
AI_tbl = [("月額費用推定", 1),("モデル学習", 2)]
cnt_tbl = [("地区月額費用別", 1)]




def run_child_window(script_name, success_message, error_message):
    try:
        subprocess.Popen([sys.executable, str(APP_DIR / script_name)], cwd=APP_DIR)
        res_area.configure(text=success_message)
    except Exception as e:
        tkMB.showerror("実行エラー", str(e))
        res_area.configure(text=error_message)


def run_child_wait(script_name, success_message, error_message):
    res = subprocess.run(
        [sys.executable, str(APP_DIR / script_name)],
        cwd=APP_DIR,
        capture_output=True,
        text=True
    )
    if res.returncode == 0:
        res_area.configure(text=success_message)
    else:
        res_area.configure(text=error_message)


def bukken_kanri():
    if v0.get() == 1:
        run_child_window("bukken_load_3.py", "テーブルロード起動", "テーブルロード異常")

    elif v0.get() == 2:
        res_area.configure(text="個別処理停止中")

    elif v0.get() == 3:
        res_area.configure(text="一括処理停止中")

    elif v0.get() == 4:
        res_area.configure(text="検索・変更処理停止中")

    elif v0.get() == 5:
        res_area.configure(text="処理停止中")

    else:
        res_area.configure(text="対象処理なし")





#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# def bukken_kanri():
#     if v0.get() == 1:
#         res_area.configure(text="ロード処理停止中")

        
#     elif v0.get() == 2:
#         res_area.configure(text="個別処理停止中")
#     elif v0.get() == 3:
#         res_area.configure(text="一括処理停止中")
#     elif v0.get() == 4:
#         res_area.configure(text="検索・変更処理停止中")
#     elif v0.get() == 5:
#         res_area.configure(text="処理停止中")
#     else:
#         res_area.configure(text="対象処理なし")
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝        

def AI_kanri():
    if v1.get() == 1:
        run_child_window("ai_estim_2.py", "月額費用推定 起動", "月額費用推定 異常")
    elif v1.get() == 2:
        res_area.configure(text="モデル学習停止中")
    else:
        res_area.configure(text="該当処理なし")


def Master_kanri():
    if v2.get() == 1:
        run_child_wait("Rent_chiku_mg.py", "地区コード管理正常", "地区コード管理異常")
    elif v2.get() == 2:
        run_child_wait("Rent_class_mg.py", "月額費用クラス管理正常", "月額費用クラス管理異常")
    else:
        res_area.configure(text="該当マスターなし")

# def data_count():
#     if v3.get() == 1:
#         res_area.configure(text="処理停止中")    
#     else:
#         res_area.configure(text="処理異常")
def data_count():
    if v3.get() == 1:
        run_child_window("Bukken_cnt_1.py", "地区月額費用別 起動", "処理異常")
    else:
        res_area.configure(text="処理異常")


def owari():
    root.destroy()


# 表示定義　タイトル    
root = tk.Tk()
root.geometry("800x600")
root.title("賃貸情報提供システム")
# DPI固定
root.tk.call('tk', 'scaling', 1.0)
tk.Label(root,text="　賃貸情報提供システム職員用メニュー　", fg = "light green", bg = "dark green", font=("Helvetica", "18", "bold italic")).pack()

# 終了ボタン
button_E = tk.Button(root,text="　終了　", bg = "yellow2", fg = "red", font=("",14, "bold italic"), command=owari)
button_E.place(x=640, y=520)

# フレームLEFT作成
Frm0 = tk.Frame(root, width=222, height= 280, bg = "light sky blue")
Frm0.place(x=30, y=100)
v0 = tk.IntVar()
L0 = tk.Label(Frm0,text="物件情報テーブル管理", padx = 5, bg = "light sky blue", font=("","12","bold"))
L0.place(x=45, y=5)

for shori_name, val0 in bukken_tbl:
    R0 = tk.Radiobutton(Frm0, text=shori_name, font=("12"), indicatoron=0, width=14,padx=5, variable=v0, command=bukken_kanri,value=val0)
    R0.place(x=30, y=5+val0*45)

# フレームCENTER作成    
Frm1 = tk.Frame(root, width=220, height= 280, bg = "light sky blue")
Frm1.place(x=285, y=100)

v1 = tk.IntVar()
L1 = tk.Label(Frm1,text="ＡＩ管理", padx = 20, bg = "light sky blue", font=("","12","bold"))
L1.place(x=60, y=5)
for doc_name, val1 in AI_tbl:
    R1 = tk.Radiobutton(Frm1, text=doc_name, font=("12"), indicatoron=0, width=14, padx=5, variable=v1, command=AI_kanri,value=val1)
    R1.place(x=30, y=5+val1*45)   
    
# フレームRIGHT_upper作成
Frm2 = tk.Frame(root, width=220, height= 140, bg = "light sky blue")
Frm2.place(x=540, y=100)
v2 = tk.IntVar()
L2 = tk.Label(Frm2,text="マスターテーブル管理", padx = 2, bg = "light sky blue", font=("","12","bold"))
L2.place(x=45, y=5)
for mst_name, val2 in Master_tbl:
    R2 = tk.Radiobutton(Frm2, text=mst_name, font=("12"), indicatoron=0, width=14,padx=5, variable=v2, command=Master_kanri,value=val2)
    R2.place(x=30, y=5+val2*45)

# フレームRIGHT_lower作成    
Frm3 = tk.Frame(root, width=220, height= 120, bg = "light sky blue")
Frm3.place(x=540, y=260)
v3 = tk.IntVar()
L3 = tk.Label(Frm3,text="データ件数管理", padx = 20, bg = "light sky blue", font=("","12","bold"))
L3.place(x =45, y=5)
for cnt_name, val3 in cnt_tbl:
    R3 = tk.Radiobutton(Frm3, text=cnt_name, font=("12"), indicatoron=0, width=14, padx=5, variable=v3, command=data_count,value=val3)
    R3.place(x=30, y=5+val3*45)   


#レスポンスメッセージエリア
res_area = tk.Label(root,width=32,height=3,text="    ", bg="pink",relief=tk.SUNKEN,font=("16"))
res_area.place(x=180,y=500)


root.mainloop()

# In[ ]:

