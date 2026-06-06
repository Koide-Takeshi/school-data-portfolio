■開発環境
OS : Windows 11 Pro 25H2
Python : 3.9.25

■前提ライブラリ
requirements.txtを参照すること。

■実行手順
1.sites_data_count.batを編集する(2か所)
  ・7行目:set "CONDA_ROOT=%USERPROFILE%\anaconda3"
　  CONDA_ROOTにanaconda3のインストールパスを設定する。(4D教室内のPCであれば編集不要)

  ・23行目:call conda activate jugyo2
    自身の仮想環境名に修正。(jugyo2部分を編集)

2.sites_data_count.batを実行

■オプション機能(exe実行では非対応)
オプション機能を有効にする場合、上記■実行手順で追加の操作を行う。
以下の環境変数をTrueにセットしている行(10～14行目)をコメントアウト解除する。(REMを削除)

・f_display_ui : GUIによる表示・操作の有効/無効
  False:無効(デフォルト)、 True:有効

・f_ng_word: 形態素解析で除外したいワードをテキストファイルから取り込むか
  False:無効(デフォルト)、 True:有効

・f_use_db : DBを辞書として使用するか切り替え
  False:未使用(デフォルト)、 True:使用

・f_csv2db : 辞書csvの内容で、辞書DBを上書き
  False:未使用(デフォルト)、 True:使用

・f_add_dic: DBを辞書とする際、テキストファイルから単語を登録するか
  False:無効(デフォルト)、 True:有効

(特記事項)環境変数を設定する際、(環境変数名)=True/Falseの「=」前後にスペースを空けないこと。