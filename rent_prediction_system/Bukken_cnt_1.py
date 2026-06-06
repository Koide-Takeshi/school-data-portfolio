#!/usr/bin/env python
# coding: utf-8

# In[11]:


import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk


# In[12]:


def load_cross_table():
    conn = sqlite3.connect("Rent.db")

    sql_bukken = """
    SELECT
        Bk_chikucd,
        Bk_getsu_cls
    FROM
        Bukken
    """
    
    df_bukken = pd.read_sql_query(sql_bukken, conn)
    
    sql_chiku = """
    SELECT
        Cc_code,
        Cc_name
    FROM
        Chiku_code
    """
    
    df_chiku = pd.read_sql_query(sql_chiku, conn)
    
    sql_class = """
    SELECT
        Mh_cls
    FROM
        Mhiyo_class
    """
    
    df_class = pd.read_sql_query(sql_class, conn)
    
    
    # 地区コード結合
    df = df_bukken.merge(
        df_chiku,
        left_on="Bk_chikucd",
        right_on="Cc_code"
    )
    
    # 月額費用クラス結合
    df = df.merge(
        df_class,
        left_on="Bk_getsu_cls",
        right_on="Mh_cls"
    )
    
    # 地区表示
    df["地区"] = (
        df["Bk_chikucd"].astype(str)
        + " "
        + df["Cc_name"]
    )
    
    # 月額費用クラス表示
    df["月額費用クラス"] = (
        df["Bk_getsu_cls"]
        + "クラス"
    )
    
    cross_df = pd.crosstab(
        df["地区"],
        df["月額費用クラス"],
        margins=True,
        margins_name="合計"
    )
    
    cross_df.index.name = "地区"
    cross_df.columns.name = "月額費用"
    
    # display(cross_df)
    
    conn.close()

    return cross_df


# In[13]:


def df_to_treeview(tree, df):
    # Treeview 初期化
    tree.delete(*tree.get_children())

    # 列設定
    tree["columns"] = list(df.columns)

    # 行名（index）を #0 に表示
    tree.heading("#0", text=df.index.name if df.index.name else "Index")
    tree.column("#0", width=150, anchor="center")

    # 各列の設定
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # データ挿入
    for idx, row in df.iterrows():
        tree.insert("", "end", text=str(idx), values=list(row))


# In[15]:


root = tk.Tk()
root.geometry("1200x600")

# --- Treeview の文字サイズを大きくする ---
style = ttk.Style()
style.configure("Treeview", font=("明朝", 12))          # 本文
style.configure("Treeview.Heading", font=("Meiryo", 14))  # ヘッダー

# --- タイトル ---
title_label = tk.Label(
    root,
    text="地区月額費用別",
    font=("Helvetica", "20", "bold italic"),
    bg="dark green",
    fg="light green",
    padx=20, pady=10
)

title_label.pack(pady=(50, 30))  # 上20px、下40px の余白

# --- エラー表示 ---
error_var = tk.StringVar()
error_label = tk.Label(
    root,
    textvariable=error_var,
    bg="#FFC0CB",
    padx=10,
    pady=5,
    width=80,
    height=3,
    relief="groove",
    bd=1,
    font=("Meiryo", 12)
)

# error_label の下端を y=550 に揃える
error_label.place(x=43, y=470)

# --- クロス表を読み込んで表示 ---
# cross_df = load_cross_table()

tree = ttk.Treeview(root, height=12)
tree.pack(padx=10,pady=40)
try:
    cross_df = load_cross_table()  # ← DB接続を含む
    df_to_treeview(tree, cross_df)
    error_var.set("DB接続成功")
    error_label.config(fg="black")
except Exception as e:
    error_var.set(f"DB接続エラー: DBに接続できませんでした")# 5/27変更
    error_label.config(fg="red")

# df_to_treeview(tree, cross_df)

# 列幅を広げる（必要なら）
for col in tree["columns"]:
    tree.column(col, width=160)

# --- 終了ボタン ---
exit_btn = tk.Button(
    root,
    text="終了",
    bg="yellow",
    fg="red",
    width=10,
    height=2,
    font=("", 14 ,"bold italic"),
    command=root.destroy
)

# ボタンの下端も y=550 に揃える
exit_btn.place(x=1000, y=490)  # ← ここを調整

root.mainloop()


# In[10]:


# root = tk.Tk()
# root.geometry("1200x600")

# # --- Treeview の文字サイズを大きくする ---
# style = ttk.Style()
# style.configure("Treeview", font=("明朝", 12))          # 本文
# style.configure("Treeview.Heading", font=("Meiryo", 14))  # ヘッダー

# # --- タイトル ---
# title_label = tk.Label(
#     root,
#     text="地区月額費用別",
#     font=("Helvetica", "20", "bold italic"),
#     bg="dark green",
#     fg="light green",
#     padx=20, pady=10
# )

# title_label.pack(pady=(50, 30))  # 上20px、下40px の余白

# # --- エラー表示 ---
# error_var = tk.StringVar()
# error_label = tk.Label(
#     root,
#     textvariable=error_var,
#     bg="#FFC0CB",
#     padx=10,
#     pady=5,
#     width=80,
#     height=3,
#     relief="groove",
#     bd=1,
#     font=("Meiryo", 12)
# )

# # error_label の下端を y=550 に揃える
# error_label.place(x=43, y=470)

# # --- クロス表を読み込んで表示 ---
# cross_df = load_cross_table()

# tree = ttk.Treeview(root, height=12)
# tree.pack(padx=10,pady=40)
# try:
#     cross_df = load_cross_table()  # ← DB接続を含む
#     df_to_treeview(tree, cross_df)
#     error_var.set("DB接続成功")
#     error_label.config(fg="black")
# except Exception as e:
#     error_var.set(f"DB接続エラー: {e}")
#     error_label.config(fg="red")

# df_to_treeview(tree, cross_df)

# # 列幅を広げる（必要なら）
# for col in tree["columns"]:
#     tree.column(col, width=160)

# # --- 終了ボタン ---
# exit_btn = tk.Button(
#     root,
#     text="終了",
#     bg="yellow",
#     fg="red",
#     width=10,
#     height=2,
#     font=("", 14 ,"bold italic"),
#     command=root.destroy
# )

# # ボタンの下端も y=550 に揃える
# exit_btn.place(x=1000, y=490)  # ← ここを調整

# root.mainloop()


# In[ ]:




