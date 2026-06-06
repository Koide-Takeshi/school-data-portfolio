# Portfolio Projects

学校の授業で制作したグループ課題をもとに、担当範囲を中心に個人でブラッシュアップしたポートフォリオです。

## 制作後のブラッシュアップ方針

グループ制作では分担して動くものを作ることを優先しました。ポートフォリオ化では、担当範囲を明確にしたうえで、実行環境に依存しにくいパス指定、GUIからのエラー表示、出力ファイルの見やすさなど、実務で使う時に困りやすい点を小さく改善しています。

## GitHub公開用の整理

授業中の作業履歴、キャッシュ、生成済みの出力ファイル、大型のexe/zipはGit管理対象外にしています。公開リポジトリには、完成版のソースコード・README・実行に必要な小さなデータを中心に載せる構成です。

## プロジェクト一覧

### [sites_data_count_project](./sites_data_count_project/00_START_HERE.md)
Webサイトのテキストデータを収集し、日本語形態素解析（Janome）で名詞を抽出・集計するツール。  
**技術:** Python / Janome / SQLite / openpyxl

**担当:** 形態素解析  
**制作後の改善:** 辞書/NGワード設定の整理、HTTPエラー処理、Excel出力の見やすさ改善

---

### [rent_prediction_system](./rent_prediction_system/README.md)
不動産物件のデータベース管理システム。XGBoostによる家賃推定AI機能を搭載。  
**技術:** Python / XGBoost / SQLite / Tkinter

**担当:** GUI画面・画面遷移まわり  
**制作後の改善:** 子画面起動の安定化、モデルファイル不足時のGUIエラー表示、検索結果テーブル定義の整理

## 読み方

まずこのREADMEで全体像を確認し、各プロジェクトのREADMEで担当範囲・改善点・実行方法を確認できる構成にしています。コードを見る場合は、形態素解析側は `sites_data_count_project/01_src/sites_data_count.py`、GUI側は `rent_prediction_system/stu_menu.py` / `rent_prediction_system/stuff_menu.py` / `rent_prediction_system/ai_estim_2.py` が主な確認対象です。
