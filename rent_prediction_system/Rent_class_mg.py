#!/usr/bin/env python
# coding: utf-8

# In[1]:


#家賃クラステーブル管理
# Mhiyo_class_mg.py

import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox as tkMB
from tkinter import ttk

# クリア処理
def g_clear():
    ycls_etr.delete(0, tk.END)
    min_etr.delete(0, tk.END)
    max_etr.delete(0, tk.END)
    ycls_etr.focus_set()
    tree_ccd.delete(*tree_ccd.get_children())
    res_area.configure(text="画面クリアしました")
    
# 一覧表示
def ichiran_hyoji():
    res_area.configure(text="")
    tree_ccd.delete(*tree_ccd.get_children())
    sql = "SELECT * FROM Mhiyo_class ORDER BY Mh_cls"
    c0 = conn.execute(sql)
    for r0 in c0.fetchall():
        tree_ccd.insert(parent='', index='end', values=(r0[0],r0[1],r0[2]))
    res_area.configure(text="一覧表示処理しました")
    
# 新規登録
def toroku():
    res_area.configure(text="")
    in_cls = ycls_etr.get()
    c1 = conn.execute("SELECT * FROM Mhiyo_class WHERE Mh_cls = ?", (in_cls,))
    r1 = c1.fetchone()
    if r1 == None:
        in_min = min_etr.get()
        in_max = max_etr.get()
        conn.execute("INSERT INTO Mhiyo_class VALUES(?,?,?)", (in_cls, in_min, in_max))
        res_area.configure(text="新規登録しました")
    else:
        res_area.configure(text="家賃クラス既存")
    ycls_etr.focus_set()

# 変更
def henko():
    res_area.configure(text="")
    in_cls = ycls_etr.get()
    c2 = conn.execute("SELECT * FROM Mhiyo_class WHERE Mh_cls = ?", (in_cls,))
    r2 = c2.fetchone()
    if r2 != None:
        in_min = min_etr.get()
        in_max = max_etr.get()
        conn.execute("REPLACE INTO Mhiyo_class VALUES(?,?,?)", (in_cls, in_min, in_max))
        res_area.configure(text="変更しました")
    else:
        res_area.configure(text="当該家賃クラスなし")
    ycls_etr.focus_set()

# 削除
def rec_del():
    res_area.configure(text="")
    in_cls = ycls_etr.get()
    c3 = conn.execute("SELECT * FROM Mhiyo_class WHERE Mh_cls = ?", (in_cls,))
    r3 = c3.fetchone()
    if r3 != None:
        if tkMB.askyesno("確認", "本当に削除しますか？"):
            tkMB.showwarning("Yes", "該当レコードは削除されました")
            conn.execute("DELETE FROM Mhiyo_class WHERE Mh_cls = ?", (in_cls,))
            g_clear()
        else:
            tkMB.showinfo("いいえ", "削除はキャンセルされました")
    else:
        res_area.configure(text="当該家賃クラスなし")
    ycls_etr.focus_set()

# 終了処理
def all_end():
    conn.close()
    res_area.config(text="　　　　 ")
    root.destroy()


# 表示定義　タイトル
root = tk.Tk()
root.geometry("1000x500")
root.title("月額費用クラス管理")
tk.Label(root,text="　 月額費用クラス管理  　", fg = "light green", bg = "dark green", font=("Helvetica", "20", "bold italic")).pack()

#レスポンスメッセージエリア
res_area = tk.Label(root,width=40,height=3,text="    ", bg="pink",relief=tk.SUNKEN,font=("16"))
res_area.place(x=220,y=340)

# 列の識別名を指定
column_ycls = ("月額費用クラス","以上","未満")

# データ項目
ycls_lbl = tk.Label(root, text="月額費用クラス", fg="red", font=("明朝", "16", "bold"))
ycls_etr = tk.Entry(root, width = 1, font = ("", 16))
min_lbl = tk.Label(root, text="以上", fg="blue2", font=("明朝", "16"))
min_etr = tk.Entry(root, width = 8, font =("明朝", "16"))
max_lbl = tk.Label(root, text="未満", fg="blue2", font=("明朝", "16"))
max_etr = tk.Entry(root, width = 8, font =("明朝", "16"))

# データ項目配置
ycls_lbl.place(x=160, y=80)
ycls_etr.place(x=340, y=80, height=28)
min_lbl.place(x=420, y=80)
min_etr.place(x=480, y=80, height=28)
max_lbl.place(x=640, y=80)
max_etr.place(x=700, y=80, height=28)

# Treeviewの生成
tree_ccd = ttk.Treeview(root, columns=column_ycls, height=8)
style = ttk.Style()
style.configure("Treeview.Heading", font=("Yu Mincho", 12, "bold"),foreground="black")
style.configure("Treeview", font=("Arial", 10))
# 列の設定
tree_ccd.column('#0',width=0, stretch='no')
tree_ccd.column('月額費用クラス', anchor='center',width=150)
tree_ccd.column('以上',anchor='c')
tree_ccd.column('未満',anchor='c')
# 列の見出し設定
tree_ccd.heading('#0',text='')
tree_ccd.heading('月額費用クラス', text='月額費用クラス',anchor='center')
tree_ccd.heading('以上', text='以上', anchor='center')
tree_ccd.heading('未満', text='未満', anchor='center')
# ウィジェットの配置
tree_ccd.place(x=220,y=130)

# オペレーションボタン
op_btn1 = tk.Button(root, text=" 一覧表示 ", width = 9, height = 2, font=("明朝","13","bold"),command=ichiran_hyoji).place(x=300, y=440)
op_btn2 = tk.Button(root, text=" 新規登録 ", width = 9, height = 2, font=("明朝","13","bold"),command=toroku).place(x=410, y=440)
op_btn3 = tk.Button(root, text=" 変更", width = 11, height = 2, font=("明朝","13","bold"),command=henko).place(x=520, y=440)
op_btn4 = tk.Button(root, text=" 削除 ", width = 11, height = 2, font=("明朝","13","bold"),command=rec_del).place(x=640, y=440)
op_btn5 = tk.Button(root, text=" クリア ", width = 9, height = 2, font=("明朝","13","bold"),command=g_clear).place(x=760, y=440)
op_btn6 = tk.Button(root, text=" 終了", width = 9, height = 2, bg = "yellow2", font=("明朝","13","bold"),command=all_end).place(x=870, y=440)

# ーーーーーー 処理開始　－－－－－－

conn = sq.connect("Rent.db", isolation_level = None)
conn.execute("PRAGMA foreign_keys = on")
res_area.config(text="Rent.db を開きました")

root.mainloop()


# In[ ]:





# In[ ]:




