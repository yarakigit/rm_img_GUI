# 画像ファイルをGUIで削除
-  データセット作成の際に, データセットに相応しくない画像を削除するのに使用できます。

## 実装
-   **python**
    - 使用ライブラリ
        - **tkinter** : GUIのプログラムを作るのに使用
        - **Pillow** : 画像を扱うのに使用

## 使い方
1. ライブラリをインストール
~~~zsh 
$ pip install -r requirements.txt
~~~
2. 実行
    - **in_dir** : 削除したい画像があるディレクトリのフルパス
    - **img_type** : 画像の種類
~~~zsh
$ python main.py --in_dir ./images --img_type jpg 
~~~

1. 画像を消去するなら**rm**をクリック, 消去しないなら**keep**をクリック

!(Screenshot_1.png)[./.readme_src/Screenshot_1.png]

1. [rm_file.sh](./rm_file.sh)が生成されるので実行
~~~zsh
$ ./rm_mnt.sh
~~~
