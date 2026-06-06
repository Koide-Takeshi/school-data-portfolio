#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk
import sqlite3
from pathlib import Path


# In[2]:


# ============================================================
# DBファイルパス設定
# ============================================================
APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "Rent.db"

RESULT_COLUMNS = [
    ("Bk_chikucd", "地区コード", 100),
    ("Bk_num", "連番", 80),
    ("Bk_ym", "登録年月", 80),
    ("Bk_yachin", "家賃", 80),
    ("Bk_kanrihi", "管理費", 80),
    ("Bk_getsu_cls", "月額クラス", 90),
    ("Bk_siki", "敷金", 80),
    ("Bk_rei", "礼金", 80),
    ("Bk_menseki", "面積", 80),
    ("Bk_chikunen", "築年数", 70),
    ("Bk_ekitoho", "最短駅徒歩分", 110),
    ("Bk_madori", "間取", 80),
    ("Bk_kaisu", "階数", 70),
    ("Bk_tatemonokai", "建物階数", 80),
    ("Bk_internet", "ｲﾝﾀｰﾈｯﾄ", 70),
    ("Bk_selflock", "ｵｰﾄﾛｯｸ", 80),
    ("Bk_hoi", "方位", 70),
    ("Bk_kozo", "構造", 70),
]


# In[3]:


def get_conn():
# # SQLアクセス処理　元
    # try :
        # conn = sqlite3.connect(DB_PATH)
        # return conn
    # except Exception as e:
        # return None
# 修正版
    try:
        return sqlite3.connect(DB_PATH)
    except Exception as e:
        # GUI に伝えるために例外を投げ直す
        raise RuntimeError(f"DB接続エラー: {e}")


# In[4]:


def Area_code():
    # conn = get_conn()
    # cur = conn.cursor()
    
    # cur.execute("SELECT * FROM Chiku_code")
    # rows = cur.fetchall()
    
    # # "code:name" の形に変換
    # values = [f"{row[0]}:{row[1]}" for row in rows]
    
    # conn.close()
    # return values
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM Chiku_code")
        rows = cur.fetchall()
        
        values = [f"{row[0]}:{row[1]}" for row in rows]
        return values

    except Exception as e:
        # ★ GUI 側で拾えるように例外を投げ直す
        raise RuntimeError(f"DB接続エラー（Area_code）: {e}")

    finally:
        try:
            conn.close()
        except:
            pass


# In[5]:


# def Mhiyo_code():
    # conn = get_conn()
    # cur = conn.cursor()
    # 
    # cur.execute("SELECT * FROM Mhiyo_class")
    # rows2 = cur.fetchall()
    # conn.close()
# 
    # values = []
# 
    # for row2 in rows2:
        # code = row2[0]
        # item2 = row2[1]
        # item3 = row2[2]
# 
        # # ★ 3項目目を空白にしたい条件（例：code が "9999999" のとき）
        # if str(item3) == "9999999":
            # item3 = ""
# 
# 
        # # ★ item3 が空でも必ず「～」を付ける
        # text = f"{code}:{item2}～{item3}"
# 
        # values.append(text)
# 
    # values.sort()
# 
    # return values

def Mhiyo_code():
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM Mhiyo_class")
        rows2 = cur.fetchall()

        values = []
        for row2 in rows2:
            code = row2[0]
            item2 = row2[1]
            item3 = row2[2]

            if str(item3) == "9999999":
                item3 = ""

            text = f"{code}:{item2}～{item3}"
            values.append(text)

        values.sort()
        return values

    except Exception as e:
        # ★ GUI 側で拾えるように例外を投げ直す
        raise RuntimeError(f"DB接続エラー（Mhiyo_code）: {e}")

    finally:
        try:
            if conn:
                conn.close()
        except:
            pass


# In[6]:


# ============================================================
# ③ 物件情報テーブル  条件検索
#    テーブル名  : Bukken（物件情報）
#                 Chiku_code（地区コード）   ← JOIN
#                 Mhiyo_class（月額費用クラス）← JOIN
#    引数        : Cc_code   地区コード（int）
#                 Mh_cls    月額費用クラス記号（str）
# ============================================================
def get_bukken_by_chiku_and_cls(Cc_code: int, Mh_cls: str) -> list[dict]:
    """地区コードと月額費用クラスで物件情報を検索して返す

    Args:
        Cc_code : 地区コード        例） 101
        Mh_cls  : 月額費用クラス記号 例） 'B'

    Returns:
        条件に合う物件情報のリスト（dict のリスト）
        ヒットなし・取得失敗 の場合は空リスト []
    """
    conn = None
    try:
        conn = get_conn()
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()

        # プレースホルダー「?」で Cc_code と Mh_cls を安全に渡す
        sql = """
            SELECT
                c.Cc_name            AS 地区名,
                m.Mh_cls             AS 月額クラス,
                b.Bk_chikucd,
                b.Bk_num,
                b.Bk_ym,
                b.Bk_yachin,
                b.Bk_kanrihi,
                b.Bk_getsu_cls,
                b.Bk_siki,
                b.Bk_rei,
                b.Bk_menseki,
                b.Bk_chikunen,
                b.Bk_ekitoho,
                b.Bk_madori,
                b.Bk_kaisu,
                b.Bk_tatemonokai,
                b.Bk_internet,
                b.Bk_selflock,
                b.Bk_hoi,
                b.Bk_kozo
            FROM   Bukken       b
            JOIN   Chiku_code   c  ON b.Bk_chikucd   = c.Cc_code
            JOIN   Mhiyo_class  m  ON b.Bk_getsu_cls = m.Mh_cls
            WHERE  b.Bk_chikucd   = ?    -- 引数: Cc_code
            AND    b.Bk_getsu_cls = ?    -- 引数: Mh_cls
            ORDER BY b.Bk_num
        """
        data = (Cc_code, Mh_cls)    # タプルでプレースホルダーに渡す

        cur.execute(sql, data)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    except Exception as e:
        raise RuntimeError(f"DB接続エラー: {e}")


    finally:
        if conn:
            conn.close()


# In[7]:


root = tk.Tk()
root.title("顧客テーブル管理")
root.geometry("500x250")

def init_root(error_var, cc, mc):
    error_var.set("")
    cc.set("")
    mc.set("")

def result_view(chiku, mhiyo):
    # args
    # chiku  : 「:」区切りで地区コード、地区名を連結した文字列
    # mhiyo  : 「:」区切りで月額費用クラス、(下限、上限)を連結した文字列
    chiku_code  = chiku.split(":")[0]
    mhiyo_class = mhiyo.split(":")[0]
    bukken_dic = get_bukken_by_chiku_and_cls(chiku_code,mhiyo_class)
    result_win = tk.Toplevel(root)
    result_win.title('result')
    result_win.geometry('1600x1000')

    # フォントサイズを変更
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12, "bold"))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  
    
    # ボタンイベント
    def on_rsrch_button_click():
        result_win.destroy()
        root.deiconify()

    # ウィンドウの伸縮設定
    result_win.grid_rowconfigure(2,weight=1)
    result_win.grid_columnconfigure(0,weight=1)
    
    # フレーム設定
    result_frame = ttk.Frame(result_win)
    result_frame.grid_rowconfigure(2,weight=1)
    result_frame.grid_columnconfigure(0,weight=1)

    # Treeviewの定義
    result_tree = ttk.Treeview(result_frame, show="headings")

    result_tree["columns"] = [column for column, _, _ in RESULT_COLUMNS]
    for column, heading, width in RESULT_COLUMNS:
        result_tree.column(column, stretch=False, width=width)
        result_tree.heading(column, text=heading)

    for bukken in bukken_dic:
        result_tree.insert(
            "",
            "end",
            values=[bukken[column] for column, _, _ in RESULT_COLUMNS]
        )
    
    # Scrollbarの定義
    scrollbar_x = tk.Scrollbar(
        result_frame
      , orient = "horizontal"
      , command = result_tree.xview
    )

    scrollbar_y = tk.Scrollbar(
        result_frame
      , orient = "vertical"
      , command = result_tree.yview
    )

    # tTreeviewにScrollbarのセット
    result_tree.configure(
        xscrollcommand = scrollbar_x.set
       ,yscrollcommand = scrollbar_y.set
    )

    
    # 検索条件(地区コード:地区名、月額クラス:下限、上限)ラベル作成
    chiku_cond_label = tk.Label(
        result_win
       ,text="(地区コード:地区名)=>" + chiku
    )
    mhiyo_cond_label = tk.Label(
        result_win
       ,text="(月額費用クラス:下限～上限)=>" + mhiyo
    )
    
    # 再検索ボタン
    rsrch_button = tk.Button(
        result_win
        , text = "再検索"
        , font=("Arial", 16)
        , command=on_rsrch_button_click
    )

    # 各コンポーネントの配置
    result_frame.grid(row=2, column=0, columnspan = 2, sticky="nsew")
    chiku_cond_label.grid(row=0, column=0,sticky = "nw")
    mhiyo_cond_label.grid(row=1, column=0,sticky = "nw")
    result_tree.grid(row=2, column=0,sticky = "nsew")
    scrollbar_y.grid(row=2, column=1,sticky = "ns")
    scrollbar_x.grid(row=3, column=0,sticky = "ew")
    rsrch_button.grid(row=4, column=0,sticky = "e",padx = 5, pady = 5)

    return result_win

title_label = tk.Label(
    root,
    text="検索",
    font=("Arial", 15, "italic"),
    bg="#006400",                 
    fg="#91EE90",                 
    padx=20, pady=5               
)
title_label.place(relx=0.5, y=20, anchor="n")


# -------------------------
# エラー表示（左下固定）
# -------------------------
error_var = tk.StringVar()
error_label = tk.Label(
    root,
    textvariable=error_var,
    fg="red",
    bg="#FFC0CB",
    padx=20,
    pady=5,
    width=30,   # ← 横幅（文字数ベース）
    height=2,    # ← 高さ（行数ベース）
    relief="groove",
    bd=1
)
error_label.place(x=20, y=200)


def open_result_window():
    val_cc = cc.get()
    val_mc = mc.get()
    
    # 必須チェック
    if not val_cc:
        error_var.set("地区コードを選択してください")
        return
    if not val_mc:
        error_var.set("月額費用クラスを選択してください")
        return

    error_var.set("")
    
    # 接続できれば別ウィンドウを作る（既存関数を呼ぶ）
    try:
        win = result_view(val_cc, val_mc)

    except RuntimeError as e:
        # ★ DB接続エラーをここで表示
        error_var.set(str(e))
        return


    # 画面遷移後、コンボボックスおよび、テキストボックスをクリア
    init_root(error_var, cc, mc)
    
    # ★ 元ウィンドウを隠す（別ウィンドウ関数に書かなくてOK）
    root.withdraw()

    # ★ 別ウィンドウを閉じたら元ウィンドウを戻す
    win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), root.deiconify()))


# -------------------------
# 終了ボタン
# -------------------------
def close_app():
    root.destroy()

# -------------------------
# 上部 UI（選択欄）
# -------------------------

# 地区コード
# 地区コード（DBの情報を入れる）
tk.Label(root, text="地区コードを選択").place(x=50, y=100)
cc = ttk.Combobox(root, state="readonly")
cc.place(x=50, y=120)

# DBから値を取得してセット
# cc["values"] = Area_code()


# 月額費用クラス
tk.Label(root, text="月額費用クラスを選択").place(x=300, y=100)
mc = ttk.Combobox(root, state="readonly")
mc.place(x=300, y=120)

# mc["values"] = Mhiyo_code()

# ★ DB 接続エラーを GUI に表示する
try:
    cc["values"] = Area_code()
    mc["values"] = Mhiyo_code()

except RuntimeError as e:
    error_var.set(str(e))

except Exception as e:
    error_var.set(f"予期せぬエラー: {e}")

# -------------------------
# 右側のボタン配置
# -------------------------
tk.Button(root, text="検索", width=10,
    height=2, command=open_result_window).place(x=300, y=200)
tk.Button(root, text="終了",bg="yellow",
    fg="red",
    width=10,
    height=2, command=close_app).place(x=400, y=200)


root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


