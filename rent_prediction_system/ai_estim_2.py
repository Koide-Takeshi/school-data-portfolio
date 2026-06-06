import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
from pathlib import Path

# ============================================================
# 1. モデル・特徴量の読み込み
# ============================================================
APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "xgb_model.pkl"
FEATURES_PATH = APP_DIR / "features.pkl"


def load_model_files():
    missing_files = [str(path.name) for path in (MODEL_PATH, FEATURES_PATH) if not path.exists()]
    if missing_files:
        return None, [], "必要なファイルが見つかりません: " + ", ".join(missing_files)
    try:
        return joblib.load(MODEL_PATH), joblib.load(FEATURES_PATH), ""
    except Exception as e:
        return None, [], f"モデル読込エラー: {e}"


model, features, startup_error = load_model_files()

location_cols = sorted([c for c in features if c.startswith("所在地_")])
madori_cols   = sorted([c for c in features if c.startswith("間取_")])
locations     = [c.replace("所在地_", "") for c in location_cols]

# ============================================================
# 2. エンコードマップ
# ============================================================
kozou_map = {"木造": 0, "軽鉄": 1, "鉄骨": 2, "ALC": 3, "RC": 4}

# 表示順序を定義
madori_list = ["1R", "1K", "1DK", "1LDK", "2K", "2DK"]

# ============================================================
# 3. GUI用選択肢
# ============================================================
floor_list   = [f"{i}階" for i in range(1, 16)]
bfloor_list  = [f"{i}階" for i in range(1, 16)]
kouzou_list  = ["木造", "軽鉄", "鉄骨", "ALC", "RC"]

# ============================================================
# 4. GUI
# ============================================================
root = tk.Tk()
root.title("賃貸物件 月額費用推定システム")
root.geometry("900x800")
root.configure(bg="#dcdcdc")
root.resizable(False, False)

title_frame = tk.Frame(root, bg="green", width=500, height=55)
title_frame.place(x=200, y=20)
tk.Label(title_frame, text="賃貸物件 月額費用推定システム",
         bg="green", fg="white",
         font=("Meiryo UI", 24, "bold")
         ).place(relx=0.5, rely=0.5, anchor="center")

input_frame = tk.Frame(root, bg="#87CEFA", bd=2, relief="ridge")
input_frame.place(x=60, y=120, width=780, height=420)
tk.Label(input_frame, text="物件情報入力",
         bg="#87CEFA", fg="black",
         font=("Meiryo UI", 18, "bold")).place(x=20, y=10)

LABEL_FONT = ("Meiryo UI", 14)
ENTRY_FONT = ("Meiryo UI", 14)

def create_label(text, x, y):
    tk.Label(input_frame, text=text, bg="#87CEFA",
             font=LABEL_FONT).place(x=x, y=y)

def create_combo(values, x, y, width=18, default=None):
    var = tk.StringVar()
    cb = ttk.Combobox(input_frame, textvariable=var, values=values,
                      state="readonly", font=ENTRY_FONT, width=width)
    cb.place(x=x, y=y)
    if default in values:
        cb.set(default)
    elif values:
        cb.current(0)
    return var


def create_spinbox(x, y, from_=1, to=20, width=4, default=5, increment=1):
    var = tk.StringVar(value=str(default))
    tk.Spinbox(input_frame, from_=from_, to=to, increment=increment,
               textvariable=var, font=ENTRY_FONT, width=width).place(x=x, y=y)
    return var
    
# ---- 行1：所在地 / 間取 ----
y = 60
create_label("所在地", 40, y)
var_loc = create_combo(locations, 180, y, 10)
create_label("間取", 430, y)
var_mad = create_combo(madori_list, 550, y, 10, default="1R")
y += 50

# ---- 行2：専有面積 / 築年数 ----
create_label("専有面積", 40, y)

var_area = tk.StringVar(value="10.00")
tk.Spinbox(input_frame, from_="10.00", to="50.00", increment=0.01, format="%.2f",
           textvariable=var_area, font=ENTRY_FONT, width=6).place(x=180, y=y)

# 築年数の位置（x=430）に干渉しないよう、右隣のラベルを調整
tk.Label(input_frame, text="㎡(10〜50)", bg="#87CEFA",
         font=LABEL_FONT).place(x=270, y=y)

create_label("築年数", 430, y)
var_age = create_spinbox(550, y, from_=0, to=50, width=4, default=0, increment=1)
tk.Label(input_frame, text="年（0〜50）", bg="#87CEFA",
         font=LABEL_FONT).place(x=620, y=y)
y += 50

# ---- 行3：構造 / 駅徒歩分 ----
create_label("構造", 40, y)
var_str = create_combo(kouzou_list, 180, y, 10, default="木造")
create_label("駅徒歩分", 430, y)
var_walk = create_spinbox(550, y, from_=1, to=20, width=4, default=5)
tk.Label(input_frame, text="分（1〜20）", bg="#87CEFA",
         font=LABEL_FONT).place(x=620, y=y)
y += 50

# ---- 行4：階数 / 建物階数 ----
create_label("階数", 40, y)
var_floor = create_combo(floor_list, 180, y, 10)
create_label("建物階数", 430, y)
var_bfloor = create_combo(bfloor_list, 550, y, 10)

error_var = tk.StringVar()
tk.Label(input_frame, textvariable=error_var,
         bg="#87CEFA", fg="red",
         font=("Meiryo UI", 12, "bold")).place(x=40, y=360)
if startup_error:
    error_var.set(startup_error)

result_frame = tk.Frame(root, bg="#f4b6c2", bd=2, relief="sunken")
result_frame.place(x=200, y=555, width=500, height=100)
result_var = tk.StringVar()
tk.Label(result_frame, textvariable=result_var,
         bg="#f4b6c2", fg="black",
         font=("Meiryo UI", 18, "bold")
         ).place(relx=0.5, rely=0.5, anchor="center")

y += 50

# ---- 行5：敷金 / 礼金（0.1刻みを適用） ----
create_label("敷金", 40, y)
var_siki = create_spinbox(180, y, from_=0.0, to=6.0, width=4, default=0.0, increment=0.1)
tk.Label(input_frame, text="ヶ月（0〜6.0）", bg="#87CEFA",
         font=LABEL_FONT).place(x=250, y=y)

create_label("礼金", 430, y)
var_reiki = create_spinbox(550, y, from_=0.0, to=6.0, width=4, default=0.0, increment=0.1)
tk.Label(input_frame, text="ヶ月（0〜6.0）", bg="#87CEFA",
         font=LABEL_FONT).place(x=620, y=y)


# ============================================================
# 5. バリデーション
# ============================================================
def get_floor(var):
    return int(var.get().replace("階", ""))

def validate_inputs():
    try:
        floor  = get_floor(var_floor)
        bfloor = get_floor(var_bfloor)
        if floor > bfloor:
            error_var.set("階数は建物階数以下にしてください")
            return False
    except ValueError:
        error_var.set("階数は建物階数以下にしてください")
        return False

    try:
        area_val = float(var_area.get())
        if not (10.00 <= area_val <= 50.00):
            raise ValueError
    except ValueError:
        error_var.set("専有面積は10.00〜50.00の数値で入力してください")
        return False
        
    try:
        age_val = int(var_age.get())
        if not (0 <= age_val <= 50):
            error_var.set("築年数は0〜50の整数で入力してください")
            return False
    except ValueError:
        error_var.set("築年数は0〜50の整数で入力してください")
        return False

    try:
        walk_val = int(var_walk.get())
        if not (1 <= walk_val <= 20):
            error_var.set("駅徒歩分は1〜20の整数で入力してください")
            return False
    except ValueError:
        error_var.set("駅徒歩分は1〜20の整数で入力してください")
        return False

    try:
        siki_val = float(var_siki.get())
        if not (0.0 <= siki_val <= 6.0):
            raise ValueError
    except ValueError:
        error_var.set("敷金は0〜6.0の数値で入力してください")
        return False

    try:
        reiki_val = float(var_reiki.get())
        if not (0.0 <= reiki_val <= 6.0):
            raise ValueError
    except ValueError:
        error_var.set("礼金は0〜6.0の数値で入力してください")
        return False
    
    error_var.set("")
    return True

# ============================================================
# 6. 予測処理
# ============================================================
def on_predict():
    if model is None or len(features) == 0:
        error_var.set(startup_error or "モデルを読み込めませんでした")
        return
    if not validate_inputs():
        return
    try:
        input_data = {col: 0 for col in features}

        input_data["専有面積"] = float(var_area.get())
        input_data["築年数"]   = int(var_age.get())
        input_data["構造"]     = kozou_map[var_str.get()]
        input_data["徒歩分"]   = int(var_walk.get())
        input_data["階数"]     = get_floor(var_floor)
        input_data["建物階数"] = get_floor(var_bfloor)
        input_data["敷金"] = float(var_siki.get())
        input_data["礼金"] = float(var_reiki.get())

        loc_col = f"所在地_{var_loc.get()}"
        mad_col = f"間取_{var_mad.get()}"
        if loc_col in input_data:
            input_data[loc_col] = 1
        if mad_col in input_data:
            input_data[mad_col] = 1

        input_df = pd.DataFrame([input_data])[features]
        pred = model.predict(input_df)[0]
        result_var.set(f"予測月額合計\n{pred:,.0f} 円")

    except Exception as e:
        messagebox.showerror("入力エラー", str(e))

# ============================================================
# 7. ボタン
# ============================================================
tk.Button(root, text="月額費用推定",
          font=("Meiryo UI", 18, "bold"),
          bg="white", width=18, height=2,
          command=on_predict).place(x=180, y=675)

tk.Button(root, text="終了",
          font=("Meiryo UI", 18, "bold"),
          bg="yellow", width=10, height=2,
          command=root.destroy).place(x=560, y=675)

root.mainloop()
