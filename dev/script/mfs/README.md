マテリアル開発環境
===

# 概要

* Python上でマテリアル関数/マテリアルをコーディング
* 全てコマンドラインで完結
* ユニットテストの実装も可

# 依存モジュール

* tranp
* NumPy

# データフロー

* C++へのトランスパイルを仲介してYAMLに変換
* 変換したYAMLを全て結合し、マスターデータとしてJSONに変換
* UEのコマンドラインからスクリプトを実行し、マテリアル関数/マテリアルアセットを生成

```
Python -> YAML -> JSON -> uasset
```

# 使用方法

## 1. トランスパイル

* `bin/script.sh mfs`
* `bin/master.sh mfs`

## 2. マテリアル関数生成

* `UnrealEditor-Cmd.exe LimitedWorld.uproject -run=FDevAssetMakerCommandlet -Maker="mfs"`

# 特記事項

## 関数名の命名規則

* 書式: `(func|material).{category}/{filename}#{category}_{func_name}`
* 例:
  * `func.op.mfs_op#op_le` -> `func/op/op_le.asset`
  * `func.op.mfs_op_bit#op_bit4_on` -> `func/op/op_bit4_on.asset`
  * `func.color.mfs_color#color_gradation` -> `func/color/color_gradation.asset`
  * `material.ui#ui_master` -> `material/ui/ui_master.asset`
* 説明: 関数名からアセットパスを補完する必要があるため、関数名とアセットのファイルパスに相関性が必要

## インポート

* トランスパイル時にインポートを元に依存モジュールを洗い出し`depends`属性を自動的に生成
* この属性を元に[mfs_loader.py](../bin/loader/mfs_loader.py)内でモジュールをソートしてマスターを生成

## 関数のハッシュ値

* [mfs_loader.py](../bin/loader/mfs_loader.py)内で関数の属性(`hash`)としてを自動的に付与
* これを基に更新可否を判定

## レイヤー/公開パラメーターの自動展開

* [mfs_config.yml](mfs_config.yml)の設定に則り展開される

### 1. レイヤー関数

* タイミング: トランスパイル時に展開
* 概要: 末尾にタグ名を持つ関数をレイヤー数分複製
* 関数名の例: `layer_{タグ名}`
* 参考: [function.j2](template/function/function.j2)

### 2. 公開パラメーター

* タイミング: マスターデータ出力時に展開
* 概要: 公開パラメーター用関数のステートメントを取り込み
* 参考: [mfs_loader.py](../bin/loader/mfs_loader.py)

## 実数の範囲

* Pythonのjsonモジュールは実数部の0が4個以上になると指数表記に変えてしまう(0.00001)
* C++のJsonモジュールが指数表記に対応していないため、0は3個までとする(0.0001)

## プロクシー関数

* 対応するノードがC++側で公開されていない関数を使う場合はプロクシー関数の呼び出しに変換される
* 対象の関数
  * `atan2_fast`: C++非公開
  * `rand_fast`: HLSL限定
  * `rgb_to_srgb`: BP限定
  * `srgb_to_rgb`: BP限定
  * `sign`: C++非公開

# 書式

## 定数/変数

### bool

* 概要: `bool`の定数式
* 書式: `bool`
* ソース: `False`
* 変換例: `false`

### float

* 概要: `float`の定数式
* 書式: `float`
* ソース: `0.0`
* 変換例: `0.0`

### ベクトル(定数)

* 概要: ベクトルの定数式
* 補足: 引数に定数のみ指定した場合
* 書式: `float[2|3|4](number...)`
* ソース: `float2(0.0, 0.0)`
* 変換例: `float2: [0.0, 0.0]`

### ベクトル(変数)

* 概要: ベクトルの変数式
* 補足: 引数に変数や式を指定した場合。make系の式に変換
* 書式: `float[2|3|4](exp...)`
* ソース: `float2(x, y)`
* 変換例: `make_float2: [x, y]`

### テクスチャーオブジェクト

* 概要: テクスチャーオブジェクト式
* 補足: パスは`image/texture/${src}`として扱う。UE系のリソースはパス解釈の都合上使えないため、ローカルにコピーが必要
* 書式: `texture('src')`
* ソース: `texture('T_Noise01')`
* 変換例: `texture: [T_Noise01]`

### 公開パラメーター

* 概要: 公開パラメーター式
* 補足: クラス変数として定義。名前が必須のため、公開パラメーターと変数宣言を兼ねる
* 補足2: 名前を基にグループ名が決定 @see [グループ名の決定規則](#グループ名の決定規則)
* 補足3: 名前を基にパラメーターIDが決定(MD5ハッシュ値)
* 書式: `var = ME.ex_[bool|float|float3|texture](args..., 'desc')`
* ソース: `a_flag_polygon: ClassVar[bool] = ME.ex_bool(True, '多角形有効化')`
* 変換例: `var: [a_flag_polygon, ex_bool: [_flag_polygon, _flag, "{md5_hash}", true, '多角形有効化']]`

## 算術演算

* 概要: 算術演算式
* 書式: `a [+-*/%] b`
* ソース: `a + b`
* 変換例: `add: [a, b]`

## 比較演算

* 概要: 比較演算式
* 補足: op系の式に変換
* 書式: `float(a [<|>|<=|>=] b)`
* ソース: `float(a <= max)`
* 変換例: `op_le: [a, max]`

## 単項演算

### 符号反転

* 概要: -1の掛け算の式に変換
* 補足: 定数の場合は`float`の定数式として扱われる
* 書式: `-exp`
* ソース: `-value`
* 変換例: `mul: [value, -1.0]`

### ビット反転

* 概要: 0と1を反転する式に変換
* 補足: 反転する値は必ず0か1である必要がある
* 書式: `float(not bit)`
* ソース: `float(not on_linear)`
* 変換例: `op_not: [on_linear]`

## 3項演算

* 概要: スイッチ式
* 補足: 条件には`bool`型の変数のみ指定が可能
* 書式: `then if flag else reject`
* ソース: `mask_linear(distance, size)[0] if flag else 1.0`
* 変換例: `ternary: [get: [call: [mask_linear: [distance, size]], 0], 1.0, flag]`

## 代入

### ローカル変数

* 概要: 代入式
* 書式: `var = exp`
* ソース: `a = b`
* 変換例: `var: [a]`

### ローカル変数(分割代入)

* 概要: 分割代入式
* 補足: 右辺はユーザー定義関数のみが対象
* 書式: `a, b, c = user_func(args...)`
* ソース: `mask, alpha = mask_linear(distance, size)`
* 変換例: `vars: [mask, alpha, mask_linear: [distance, size]]`

## 関数コール

### ユーザー定義関数

* 概要: ユーザー定義関数コール式
* 補足: 使用する戻り値を明示した場合は`get`でラップされる
* 書式: `user_func(args...)`
* ソース: `opacity * mask_linear(distance, size)[0]`
* 変換例: `mul: [opacity, get: [call: [distance, size], 0]]`

### ライブラリー関数

* 概要: ライブラリー関数コール式
* 書式: `ME.xxx(args...)`
* ソース: `ME.cos(degree, 360.0)`
* 変換例: `cos: [degree, 360.0]`

### ベクトルメソッド

* 概要: ライブラリー関数コール式に変換
* 書式: `v.method(args...)`
* ソース: `v.dot(v2)`
* 変換例: `dot: [v, v2]`

### PI

* 概要: PI定数式
* 書式: `ME.pi()`
* ソース: `ME.pi()`
* 変換例: `pi: []`

## プロパティー

* 概要: mask式
* 補足: ベクトル/テクスチャー型が対象
* 書式: `v.[x|y|z|w|xy|xyz]`
* ソース: `vector.x`
* 変換例: `mask: [vector, x]`

## 戻り値

### 単体(式)

* 概要: returns式(単体)
* 補足: 名前は`result`固定
* 書式: `return exp`
* ソース: `return a * 2.0`
* 変換例: `returns: [result, mul: [a, 2.0], 'コメント']`

### 複数(tuple)

* 概要: returns式(複数)
* 補足: 名前が必須なため、変数参照だけにする
* 書式: `return vars...`
* ソース: `return mask, alpha`
* 変換例:

```yaml
returns: [mask, mask, 'コメント1']
returns: [alpha, alpha, 'コメント2']
```

## 関数定義

* 概要: 関数宣言式
* 補足: DocString、引数のデフォルト値、戻り値は必須
* 書式: `def func_name(params...) -> types...: ...`
* ソース:

```python
def mask_linear(distance: float = preview_distance(), size: float = 1.0) -> tuple[float, float]:
  """線形マスクを生成

  Args:
    distance: 距離
    size: 径
  Returns:
    (マスク, 距離)
  """
  ...
  return mask, out_distance
```

* 変換例:

```yaml
mask_linear:
  desc: '線形マスクを生成'
  params:
    - param: [float, distance, preview_distance: [], '距離']
    - param: [float, size, 1.0, '径']
  statements:
    ...
    - returns: [mask, mask, 'マスク']
    - returns: [out_distance, out_distance, '距離']
```

## その他

* `assert`は削除
* `group`は評価順序にのみ影響するため削除
* DocStringの区切り文字に`|`を使うため、コメントに`|`は入れられない
* クラスは公開パラメーターの定義領域としてのみ利用

### グループ名の決定規則

* パターン: `^((a_)?[a-z])`
* 変換例1: `a_flag_on` -> `a_flag`
* 変換例2: `a_flag_00_on` -> `a_flag`
* 変換例3: `flag_00_on` -> `flag`
