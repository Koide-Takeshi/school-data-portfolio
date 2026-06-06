#!/usr/bin/env python
# coding: utf-8

# In[1]:


#地区コードテーブル管理
# Rent_chiku_mg.py

import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox as tkMB
from tkinter import ttk

r_k = None

# クリア処理
def g_clear():
    cd_etr.delete(0, tk.END)
    nm_etr.delete(0, tk.END)    
    cd_etr.focus_set()
    res_area.configure(text="画面クリアしました")
    
# 一覧表示
def ichiran_hyoji():
    res_area.configure(text="")
    tree_ccd.delete(*tree_ccd.get_children())
    sql = "SELECT * FROM Chiku_code ORDER BY Cc_code"
    c0 = conn.execute(sql)
    for r0 in c0.fetchall():
        tree_ccd.insert(parent='', index='end', values=(r0[0],r0[1]))
    res_area.configure(text="一覧表示処理しました")
# 検索
def kensaku():
    res_area.configure(text="")
    global r_k
    in_cd = cd_etr.get()
    c = conn.execute("SELECT * FROM Chiku_code WHERE Cc_code = ?", (in_cd,))
    r_k = c.fetchone()
    if r_k != None:
        nm_etr.insert(0, r_k[1])
    else:
        res_area.configure(text="当該地区コードなし")
    cd_etr.focus_set()
    op_btn4["state"] = "normal"
    op_btn5["state"] = "normal"

# 登録
def toroku():
    res_area.configure(text="")
    in_cd = cd_etr.get()
    c = conn.execute("SELECT * FROM Chiku_code WHERE Cc_code = ?", (in_cd,))
    r = c.fetchone()
    if r == None:
        in_nm = nm_etr.get()
        conn.execute("INSERT INTO Chiku_code VALUES(?,?)", (in_cd, in_nm))
        conn.commit()
        res_area.configure(text="新規登録しました")
    else:
        res_area.configure(text="地区コード既存")
    cd_etr.focus_set()
    
# 変更
def henko():
    global r_k
    in_cd = cd_etr.get()
    res_area.configure(text="")
    if r_k != None:
        if tkMB.askyesno("確認", "本当に変更しますか？"):
            tkMB.showwarning("Yes", "該当レコードは変更されました")
            in_nm = nm_etr.get()
            conn.execute("UPDATE Chiku_code SET Cc_name = ? WHERE Cc_code = ?", (in_nm, in_cd))            
            conn.commit()
        else:
            tkMB.showinfo("いいえ", "変更はキャンセルされました")
    else:
        res_area.configure(text="当該地区コードなし")
    cd_etr.focus_set()
    op_btn4["state"] = tk.DISABLED
    
# 削除
def rec_del():
    global r_k
    in_cd = cd_etr.get()
    res_area.configure(text="")
    if r_k != None:
        if tkMB.askyesno("確認", "本当に削除しますか？"):
            tkMB.showwarning("Yes", "該当レコードは削除されました")
            conn.execute("DELETE FROM Chiku_code WHERE Cc_code = '" + in_cd + "'")
            conn.commit()
            g_clear()
        else:
            tkMB.showinfo("いいえ", "削除はキャンセルされました")
    else:
        res_area.configure(text="当該地区コードなし")
    cd_etr.focus_set()
    op_btn5["state"] = tk.DISABLED
    
# 終了処理
def all_end():
    conn.close()
    res_area.config(text="　　　　 ")
    root.destroy()


# 表示定義　タイトル
root = tk.Tk()
root.geometry("1050x500")
root.title("地区コード管理")
tk.Label(root,text="　  地区コード管理  　", fg = "light green", bg = "dark green", font=("Helvetica", "20", "bold italic")).pack()

#レスポンスメッセージエリア
res_area = tk.Label(root,width=40,height=3,text="    ", bg="pink",relief=tk.SUNKEN,font=("16"))
res_area.place(x=240,y=340)

# 列の識別名を指定
column_ccd = ("地区コード","地区")

# データ項目
cd_lbl = tk.Label(root, text="地区コード", fg="red", font=("明朝", "16", "bold"))
cd_etr = tk.Entry(root, width = 3, font = ("", 16))
nm_lbl = tk.Label(root, text="地区", fg="blue2", font=("明朝", "16"))
nm_etr = tk.Entry(root, width = 20, font =("明朝", "16"))

# データ項目配置
cd_lbl.place(x=100, y=80)
cd_etr.place(x=240, y=80, height=28)
nm_lbl.place(x=100, y=130)
nm_etr.place(x=240, y=130, height=28)


# Treeviewの生成
tree_ccd = ttk.Treeview(root, columns=column_ccd, height=11)
style = ttk.Style()
style.configure("Treeview.Heading", font=("Yu Mincho", 12, "bold"),foreground="black")
style.configure("Treeview", font=("Arial", 10))
# 列の設定
tree_ccd.column('#0',width=0, stretch='no')
tree_ccd.column('地区コード', anchor='center',width=90)
tree_ccd.column('地区',anchor='w')

# 列の見出し設定
tree_ccd.heading('#0',text='')
tree_ccd.heading('地区コード', text='地区コード',anchor='center')
tree_ccd.heading('地区', text='地区', anchor='center')

# ウィジェットの配置
tree_ccd.place(x=520,y=80)


# オペレーションボタン
op_btn1 = tk.Button(root, text=" 一覧表示 ", width = 9, height = 2, font=("明朝","13","bold"),command=ichiran_hyoji)
op_btn1.place(x=190, y=440)
op_btn2 = tk.Button(root, text=" 新規登録 ", width = 9, height = 2, font=("明朝","13","bold"),command=toroku)
op_btn2.place(x=300, y=440)
op_btn3 = tk.Button(root, text=" 検索", width = 9, height = 2, font=("明朝","13","bold"),command=kensaku)
op_btn3.place(x=410, y=440)
op_btn4 = tk.Button(root, text=" 変更", width = 9, height = 2, font=("明朝","13","bold"),command=henko, state="disabled")
op_btn4.place(x=520, y=440)
op_btn5 = tk.Button(root, text=" 削除 ", width = 9, height = 2, font=("明朝","13","bold"),command=rec_del, state="disabled")
op_btn5.place(x=630, y=440)
op_btn6 = tk.Button(root, text=" クリア ", width = 9, height = 2, font=("明朝","13","bold"),command=g_clear)
op_btn6.place(x=740, y=440)
op_btn7 = tk.Button(root, text=" 終了", width = 9, height = 2, bg = "yellow2", font=("明朝","13","bold"),command=all_end)
op_btn7.place(x=850, y=440)

# ーーーーーー 処理開始　－－－－－－

conn = sq.connect("Rent.db", isolation_level = None)
conn.execute("PRAGMA foreign_keys = on")
res_area.config(text="Rent.db を開きました")

root.mainloop()


# In[ ]:





# In[ ]:




