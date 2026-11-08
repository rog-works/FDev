FDev
===

# 概要

* Unreal Engine用プラグイン
* [tranp](https://github.com/rog-works/tranp)を用いたPython開発環境

# 機能(プラグイン)

* Core機能
  * アセットマネージャー
  * Json
* アセット生成
  * マテリアル関数

# 必須要件

## プラグイン

* Unreal Engine >= 5.8

## Python開発環境

* Python >= 3.13
* [Lark](https://lark-parser.readthedocs.io/en/latest/index.html) >= 1.3.1
* [Jinja2](https://github.com/pallets/jinja) >= 3.1.6
* [PyYAML](https://pypi.org/project/PyYAML/) >= 6.0.3
* [NumPy](https://numpy.org/ja/) >= 2.2.5
* [tranp](https://github.com/rog-works/tranp) >= 0.9.20

# Python開発環境

## インストール

```bash
# ワークスペースに移動
$ cd path/to/FDev

# devディレクトリーに移動
$ cd dev

# 依存モジュールインストール
$ pip install -r requirements.txt -t vendor
```

## コマンド実行

```bash
$ cd dev

# トランスパイル(Python -> C++)
$ bin/transplie.sh

# マテリアル関数のマスター生成
$ bin/script.sh && bin/master.sh
```

# マテリアル関数生成

* VSCode上で「Shift + Ctrl + B」
* 表示されたメニューから「Make Asset」を選択
* 完了すると「Build success!」という通知が表示

# 互換性

* 本リポジトリーは実験的なプロジェクトであり、作者自身の課題を解決するために開発しています
* 事前の告知なく破壊的な仕様変更を行う可能性があり、バージョン毎の動作・互換性を保証するものではない旨、予めご理解ください
* 継続的な利用にあたってはバックアップを推奨します

# ライセンス

* [MIT](LICENCE)
* 本リポジトリー内の既存の成果物に関してはライセンスに従います
* 本リポジトリーを利用し、独自に生成した成果物に関してはライセンスに含みません
