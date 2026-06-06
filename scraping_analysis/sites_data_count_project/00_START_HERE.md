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
└──03_data/                                   # データ入出力
    ├── dictionaries/                         # プログラムのInputファイル
    │   ├── janome_dic.csv                    # janome辞書データ(CSV)
    │   ├── ng_word.txt                       # NGワード設定用テキストファイル
    │   └── add_dicword.txt                   # 辞書への追加設定用テキストファイル
    └── output/                               # プログラムのOutputファイル
        └── README_program_output_files.md    # 出力ファイルの説明

```
GitHub公開用に、exe・Notebook・実行済みoutputファイルは退避しています。

## 各フォルダの役割

### `01_src/` — Python ソースコード
**最終提出する Python ソースコード**を置く場所。 `sites_data_count.py` をここに配置する。Notebook で試行錯誤した後、安定したコードを `.py` に変換してここに集約する。

### `03_data/` — データ入出力
入力データと出力データを物理的に分離。

- **`dictionaries/`**: Janome のカスタム辞書 CSV。`iPhone 14 Pro` を1単語として扱うためのユーザー定義語などを格納(プログラムへの「入力」)。
- **`output/`**: プログラム実行で生成されるファイル(Excel・DB)。実行後に `sites_data_count.xlsx` と `sites_data_count.db` が出力される。
