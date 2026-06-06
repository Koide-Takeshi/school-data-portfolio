#!/usr/bin/env python
# coding: utf-8

# In[15]:


#!/usr/bin/env python
# coding: utf-8

import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# ==========================================
# DBファイル
# ==========================================
DB_NAME = "Rent.db"


class BukkenLoadApp:

    # ==========================================
    # 初期化
    # ==========================================
    def __init__(self, root):

        self.root = root
        self.root.title("④ 物件テーブルロードプログラム")
        self.root.geometry("700x520")

        # -----------------------------
        # タイトル
        # -----------------------------
        title_label = tk.Label(
            root,
            text="物件情報テーブル 再ロード処理",
            font=("Helvetica", 14, "bold"),
            fg="light green",
            bg="dark green")
        title_label.pack(pady=10)

        # -----------------------------
        # CSVファイル
        # -----------------------------
        file_frame = tk.Frame(root)
        file_frame.pack(pady=15, fill="x", padx=20)

        lbl_file = tk.Label(
            file_frame,
            text="入力CSVファイル名:"
        )
        lbl_file.pack(side="left")

        self.entry_filename = tk.Entry(
            file_frame,
            width=50
        )
        self.entry_filename.pack(
            side="left",
            padx=5,
            fill="x",
            expand=True
        )

        self.entry_filename.insert(
            0,
            "rent_bukken_data.csv"
        )

        btn_browse = tk.Button(
            file_frame,
            text="参照",
            command=self.browse_file
        )
        btn_browse.pack(side="left")

        # -----------------------------
        # ボタン
        # -----------------------------
      

        btn_load = tk.Button(
            root,
            text="ロード",
            width=12,
            font=("Helvetica", 11, "bold"),
            command=self.click_load)
        btn_load.place(x=450,y=430)

        btn_exit = tk.Button(
            root,
            text="終了",
            width=12,
            font=("Helvetica", 10, "bold"),
            command=self.click_exit,
            bg="yellow2",
            fg="red",
            pady=3)
        btn_exit.place(x=570,y=430)

        # -----------------------------
        # メッセージエリア
        # -----------------------------
        

        self.txt_message = tk.Text(
            root,
            bg="pink",
            relief=tk.SUNKEN,
            font=("Consolas", 10))
        self.txt_message.place(x=130,y=115,width=440,height=300)

        self.log_message("プログラムを起動しました。")

    # ==========================================
    # メッセージ表示
    # ==========================================
    def log_message(self, text):

        self.txt_message.insert(tk.END, text + "\n")
        self.txt_message.see(tk.END)

    # ==========================================
    # CSVファイル参照
    # ==========================================
    def browse_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if file_path:

            self.entry_filename.delete(0, tk.END)
            self.entry_filename.insert(0, file_path)

    # ==========================================
    # DB接続
    # ==========================================
    def get_connection(self):

        return sqlite3.connect(DB_NAME)

    # ==========================================
    # ロードボタン
    # ==========================================
    def click_load(self):

        csv_filename = self.entry_filename.get().strip()

        # -----------------------------
        # ファイル存在チェック
        # -----------------------------
        if not csv_filename:

            self.log_message("【エラー】CSVファイル名が未入力です。")
            return

        if not os.path.exists(csv_filename):

            self.log_message(
                f"【エラー】CSVファイルが存在しません: {csv_filename}"
            )
            return

        # -----------------------------
        # 実行確認
        # -----------------------------
        ans = messagebox.askyesno(
            "確認",
            "物件情報テーブルを再作成します。\n本当に実行しますか？"
        )

        if ans:

            self.log_message("実行します")
            self.execute_load(csv_filename)

        else:

            self.log_message("処理をキャンセルされました。")

    # ==========================================
    # ロード処理
    # ==========================================
    def execute_load(self, csv_filename):

        conn = None

        try:

            # -----------------------------
            # CSV読込
            # -----------------------------
            self.log_message("CSV読込開始...")

            df = pd.read_csv(csv_filename)

            if df.empty:

                self.log_message("【エラー】CSVにデータがありません。")
                return

            # ==========================================
            # 高速化①
            # マスタを一括取得
            # ==========================================
            conn = self.get_connection()
            cursor = conn.cursor()

            # 地区コードマスタ
            cursor.execute("""
                SELECT Cc_code, Cc_name
                FROM Chiku_code
            """)

            chiku_master = cursor.fetchall()

            # 月額クラスマスタ
            cursor.execute("""
                SELECT Mh_cls, Mh_min, Mh_max
                FROM Mhiyo_class
                ORDER BY Mh_min
            """)

            monthly_master = cursor.fetchall()

            # ==========================================
            # 加工用
            # ==========================================
            processed_rows = []

            chiku_counters = {}

            display_counts = {}

            # ==========================================
            # CSVループ
            # ==========================================
            for index, row in df.iterrows():

                line_no = index + 2

                # -----------------------------
                # 所在地
                # -----------------------------
                location_name = str(
                    row.get("所在地", "")
                ).strip()

                # ==========================================
                # 高速化②
                # DBアクセスをやめてメモリ検索
                # ==========================================
                chiku_code = None

                for code, name in chiku_master:

                    if name in location_name:

                        chiku_code = code
                        break

                if chiku_code is None:

                    self.log_message(
                        f"【検証エラー】{line_no}行目 "
                        f"所在地[{location_name}] "
                        f"は地区コード表に存在しません。"
                    )
                    return

                # -----------------------------
                # 連番
                # -----------------------------
                chiku_counters[chiku_code] = (
                    chiku_counters.get(chiku_code, 0) + 1
                )

                bk_num = chiku_counters[chiku_code]

                # -----------------------------
                # 数値変換
                # -----------------------------
                try:

                    bk_ym = int(row.get("登録年月", 0))

                    bk_yachin = int(row.get("家賃", 0))

                    bk_kanrihi = int(row.get("管理費", 0))

                    bk_siki = float(row.get("敷金", 0))

                    bk_rei = float(row.get("礼金", 0))

                    bk_menseki = float(row.get("面積", 0))

                    bk_chikunen = int(row.get("築年数", 0))

                    bk_ekitoho = int(
                        row.get("最短駅徒歩分", 0)
                    )

                    bk_kaisu = int(row.get("階数", 0))

                    bk_tatemonokai = int(
                        row.get("建物階数", 0)
                    )

                except Exception as ex:

                    self.log_message(
                        f"【検証エラー】{line_no}行目 "
                        f"数値変換失敗: {str(ex)}"
                    )
                    return

                # ==========================================
                # 高速化③
                # 月額クラスもメモリ検索
                # ==========================================
                total = bk_yachin + bk_kanrihi

                bk_getsu_cls = "Z"

                for cls, min_val, max_val in monthly_master:

                    if max_val is None:

                        if total >= min_val:

                            bk_getsu_cls = cls
                            break

                    else:

                        if total >= min_val and total < max_val:

                            bk_getsu_cls = cls
                            break

                # -----------------------------
                # 文字列項目
                # -----------------------------
                bk_madori = str(row.get("間取", ""))

                bk_internet = str(
                    row.get("ｲﾝﾀｰﾈｯﾄ", "")
                )

                bk_selflock = str(
                    row.get("ｵｰﾄﾛｯｸ", "")
                )

                bk_hoi = str(row.get("方位", ""))

                bk_kozo = str(row.get("構造", ""))

                # -----------------------------
                # INSERT用
                # -----------------------------
                record = (
                    chiku_code,
                    bk_num,
                    bk_ym,
                    bk_yachin,
                    bk_kanrihi,
                    bk_getsu_cls,
                    bk_siki,
                    bk_rei,
                    bk_menseki,
                    bk_chikunen,
                    bk_ekitoho,
                    bk_madori,
                    bk_kaisu,
                    bk_tatemonokai,
                    bk_internet,
                    bk_selflock,
                    bk_hoi,
                    bk_kozo
                )

                processed_rows.append(record)

                # 件数表示
                display_counts[location_name] = (
                    display_counts.get(location_name, 0) + 1
                )

            # ==========================================
            # DB更新
            # ==========================================
            self.log_message(
                "データベース更新開始..."
            )

            cursor.execute("BEGIN TRANSACTION")

            # 全削除
            cursor.execute(
                "DELETE FROM Bukken"
            )

            # INSERT
            insert_sql = """
                INSERT INTO Bukken (
                    Bk_chikucd,
                    Bk_num,
                    Bk_ym,
                    Bk_yachin,
                    Bk_kanrihi,
                    Bk_getsu_cls,
                    Bk_siki,
                    Bk_rei,
                    Bk_menseki,
                    Bk_chikunen,
                    Bk_ekitoho,
                    Bk_madori,
                    Bk_kaisu,
                    Bk_tatemonokai,
                    Bk_internet,
                    Bk_selflock,
                    Bk_hoi,
                    Bk_kozo
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            cursor.executemany(
                insert_sql,
                processed_rows
            )

            conn.commit()

            # ==========================================
            # 完了表示
            # ==========================================
            self.log_message("")
            self.log_message(
                "----- ロード完了結果 -----"
            )

            for k in sorted(display_counts.keys()):

                self.log_message(
                    f"地区[{k}] : "
                    f"{display_counts[k]}件"
                )

            self.log_message(
                "--------------------------"
            )

            self.log_message(
                f"合計 {len(processed_rows)}件 "
                f"ロード完了"
            )

            messagebox.showinfo(
                "完了",
                f"{len(processed_rows)}件 "
                f"正常にロードしました。"
            )

        # ==========================================
        # DBエラー
        # ==========================================
        except sqlite3.Error as se:

            if conn:

                conn.rollback()

            self.log_message(
                f"【DBエラー】{str(se)}"
            )

        # ==========================================
        # その他エラー
        # ==========================================
        except Exception as e:

            self.log_message(
                f"【システムエラー】{str(e)}"
            )

        finally:

            if conn:

                conn.close()

    # ==========================================
    # 終了
    # ==========================================
    def click_exit(self):

        self.root.destroy()


# ==========================================
# メイン
# ==========================================
if __name__ == "__main__":

    root = tk.Tk()

    app = BukkenLoadApp(root)

    root.mainloop()


# In[ ]:





# In[ ]:




