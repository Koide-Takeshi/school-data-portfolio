# 03_data/dictionaries/ — Janome カスタム辞書

Janome の形態素解析で使うユーザー定義辞書(CSV)を置く場所。
**プログラムへの「入力」ファイル**。

## ここに置くファイル
- `janome_dic.csv` — ベース辞書
- `add_dicword.txt` — 追加辞書(iPhone 14 Pro を1単語化など、追加依頼への対応)
- `ng_word.txt` — 解析対象から除外する単語リスト

## 注意
このフォルダのファイルは手作業で編集するもの。
`f_use_db=True` と `f_csv2db=True` を指定した場合は、CSVから作業用の辞書DBを作成できる。
