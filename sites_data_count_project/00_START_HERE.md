## フォルダ構成

```
sites_data_count_project/
├── 00_START_HERE.md               　　　　　　# このファイル(構成説明)
├── readme.txt               　　　　　　      # 実行手順の説明
├── requirements.txt               　　　　　　# 依存ライブラリ
├── sites_data_count.bat           　　　　　　# 実行用batファイル
│
├── 01_src/                                   # 最終成果物のソースコード(.py)
│   └── sites_data_count.py                   # 競合サイト分析用データの自動生成プログラム
│             
├── 02_notebooks/                             # Jupyter Notebook(開発用)
│   └── sites_data_count.ipynb                # ソースコードのNotebookファイル(参考)
│             
└──03_data/                                   # データ入出力
    ├── dictionaries/                         # プログラムのInputファイル
    │   ├── janome_dic.csv                    # janome辞書データ(CSV)
    │   ├── janome_dic.db                     # janome辞書データ(DB)
    │   ├── ng_word.txt                       # NGワード設定用テキストファイル
    │   └── add_dicword.txt                   # 辞書への追加設定用テキストファイル
    └── output/                               # プログラムのOutputファイル
        ├── sites_data_count.xlsx　           # 単語と、出現回数のカウント結果(Excel)
        └── sites_data_count.db               # 単語と、出現回数のカウント結果(DB)

```

## 各フォルダの役割

### `01_src/` — Python ソースコード
**最終提出する Python ソースコード**を置く場所。 `sites_data_count.py` をここに配置する。Notebook で試行錯誤した後、安定したコードを `.py` に変換してここに集約する。

### `02_notebooks/` — Jupyter Notebook
**Jupyter Notebook での試行錯誤・検証作業**の置き場。`.ipynb` 形式のまま残す。`01_src/` の `.py` ファイルと役割を明確に分けている:
- `02_notebooks/` = 試す・確かめる(開発プロセス)
- `01_src/` = 最終的に動かす(成果物)

進捗表示の追加など、新機能を試した Notebook はここに残す。

### `03_data/` — データ入出力
入力データと出力データを物理的に分離。

- **`dictionaries/`**: Janome のカスタム辞書 CSV。`iPhone 14 Pro` を1単語として扱うためのユーザー定義語などを格納(プログラムへの「入力」)。
- **`output/`**: プログラム実行で生成されるファイル(Excel・DB)。 `sites_data_count.xlsx` がここに出力される。