.. highlight:: none

.. _Ch:Config_UHFR:

環境設定ファイル
--------------------------------

このファイルでは、TOML形式でH-waveに関する環境を設定します。
本ファイルは以下の3つのセクションから構成されます。

1. ``mode`` セクション: 計算モードに関する設定を指定するセクション。

2. ``log`` セクション: 標準出力に関する設定を指定するセクション。

3. ``file`` セクション: 入出力ファイルのパスなどを設定するセクションで、 ``input`` , ``output`` のサブセクションで構成される。

以下、ファイル例を記載します。

::

    [log]
    print_level = 1
    print_step = 20
    [mode]
    mode = "UHFr"
    [mode.param]
    Nsite = 8
    2Sz = 0
    Ncond = 8
    IterationMax = 1000
    EPS = 8
    RndSeed = 123456789
    T = 0.0
    [file]
    [file.input]
    path_to_input = ""
    OneBodyG = "greenone.def"
    [file.input.interaction]
    Trans = "trans.def"
    CoulombIntra = "coulombintra.def"
    [file.output]
    path_to_output = "output"
    energy = "energy.dat"
    eigen = "eigen"
    green = "green.dat"

ファイル形式
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TOML形式


パラメータ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``mode`` セクション
================================

- ``mode``

  **形式 :** string型

  **説明 :** 計算モードを指定します。実空間版UHFを利用する場合には ``UHFr`` と入力して下さい。

- ``flag_fock``

  **形式 :** bool型 (デフォルトは ``true`` )

  **説明 :** ``true`` の場合にはFock項を考慮し、 ``false`` の場合にはHartree項のみ取り扱います。


``mode.param`` セクション
================================

``mode.param`` セクションでは計算用のパラメータを指定します。

- ``T``

  **形式 :** float型 (デフォルトは0)

  **説明 :** 温度を指定します。0以上の値を指定してください。

- ``2Sz``

  **形式 :** int型, string型, または None (デフォルトはNone)

  **説明 :**
  スピンのz成分 ``Sz`` を固定したい場合に使用し、固定する ``Sz`` の2倍の値を指定します。
  その場合はスピン空間をupとdownに分けた上で計算を実施します。
  何も指定しない場合 ( ``None`` ) または ``"free"`` を指定した場合は、スピン空間を分けずに計算を実施します。
  ``Sz`` が保存しないような場合(スピン軌道相互作用がある場合など)には指定しないようにしてください。
  ``-Nsite`` から ``Nsite`` の値を指定してください。

- ``Nsite``

  **形式 :** int型

  **説明 :** サイトの数を指定します。1以上の値を指定してください。

- ``Ncond``

  **形式 :** int型

  **説明 :** 伝導電子の数を指定します。1以上の値を指定してください。

- ``filling``

  **形式 :** float型

  **説明 :** 伝導電子の状態数に対する占有率を指定します。0以上1以下の値を指定してください。 ``Ncond`` と同時に指定されている場合はエラーで終了します。

- ``Ncond_round_mode``

  **形式 :** str型 (デフォルトは ``"strict"``)

  **説明 :** ``filling`` から計算される伝導電子数を整数値に丸める方法を指定します。以下のいずれかの値をとります。


     - ``as-is`` : 丸めを行いません。(戻り値は float型です)
     - ``round-up`` : 小数点以下を切り上げます。
     - ``round-down`` : 小数点以下を切り捨てます。
     - ``round-off`` : 小数点以下を四捨五入します。
     - ``round``  : 小数点以下を ``round`` 関数で丸めます。0.5 は 0 に丸められるので注意。
     - ``strict`` : 整数でない場合はエラーで終了します。
     - ``exact`` : 整数でない場合は warning を表示し、 ``round`` で丸めた整数値を返します。

- ``IterationMax``

  **形式 :** int型 (デフォルトは20000)

  **説明 :** 反復回数の上限を指定します。0以上の値を指定してください。


- ``EPS``

  **形式 :** int型 (デフォルトは6)

  **説明 :** 収束条件を指定します。一つ前のステップとのグリーン関数の差のノルムが :math:`10^{\rm -EPS}` 以下になった場合に収束したと判定します。
  残差は :math:`R = \sum_{i,j}^{N}\sqrt{ \left| G_{ij}^{\rm new} - G_{ij}^{\rm old} \right|^2} / 2N^2` で定義されます。
  0以上の値を指定してください。

- ``Mix``

  **形式 :** float型 (デフォルトは0.5)

  **説明 :** Green関数の更新時に、古い値と新しく得られた値を混ぜる(simple-mixing)割合 :math:`\alpha` を指定します。
  0以上から1以下の実数で指定してください。1にすると古い値は使われません。
  simple-mixingについては :ref:`アルゴリズムの章 <algorithm_sec>` をご覧ください。


- ``RndSeed``

  **形式 :** int型 (デフォルトは1234)

  **説明 :** 乱数のシード(種)を指定します。


- ``ene_cutoff``

  **形式 :** float型 (デフォルトは100.0)

  **説明 :** Fermi分布関数を計算する際に overflow を避けるためのカットオフを指定します。

- ``strict_hermite``

  **形式 :** bool型 (デフォルトは false)

  **説明 :** 相互作用定義ファイルの読み込み時に Hermiticity を厳密にチェックします。true の場合、 ``hermite_tolerance`` 以上のズレが見つかったときはエラーで終了します。false の場合は warning を表示して実行を継続します。

- ``hermite_tolerance``

  **形式 :** float型 (デフォルトは :math:`10^{-8}`)

  **説明 :** Hermiticity の許容値 :math:`|t_{ij} - t_{ji}^*| < \varepsilon` を指定します。

``log`` セクション
================================

- ``print_level``

  **形式 :** int型 (デフォルトは1)

  **説明 :** 標準出力のレベルを指定します。1にすると詳細な情報が出力されます。

- ``print_step``

  **形式 :** int型 (デフォルトは1)

  **説明 :** 反復計算の途中に計算ログを標準出力に書き出す間隔を指定します。1以上の値を指定してください。

- ``print_check``

  **形式 :** str型

  **説明 :** 反復計算の途中に計算ログをファイルに書き出す場合、出力先ファイル名を指定します。無指定のときは出力しません。


``file`` セクション
================================

``input`` と ``output`` のサブセクションからなります。
前者は入力ファイルに関する情報(格納場所やファイル名の指定など)、後者は出力ファイルに関する情報(格納場所など)について指定します。
以下、順に説明します。

``file.input`` セクション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``path_to_input``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 入力ファイルの格納されているディレクトリを指定します。

- ``Initial``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 初期配置を指定する入力ファイル名を指定します。

- ``OneBodyG``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 出力したい一体グリーン関数を指定する入力ファイル名を指定します。

``file.input.interaction`` セクション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``Trans``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 一般的一体相互作用を記述するファイルを指定します。

- ``InterAll``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 一般的二体相互作用を記述するファイルを指定します。

- ``CoulombIntra``

  **形式 :** str型 (デフォルトは "")

  **説明 :** サイト内クーロン相互作用を記述するファイルを指定します。

- ``CoulombInter``

  **形式 :** str型 (デフォルトは "")

  **説明 :** サイト間クーロン相互作用を記述するファイルを指定します。

- ``Hund``

  **形式 :** str型 (デフォルトは "")

  **説明 :** フント結合を記述するファイルを指定します。

- ``PairHop``

  **形式 :** str型 (デフォルトは "")

  **説明 :** ペアホッピングを記述するファイルを指定します。

- ``Exchange``

  **形式 :** str型 (デフォルトは "")

  **説明 :** 交換相互作用を記述するファイルを指定します。

- ``Ising``

  **形式 :** str型 (デフォルトは "")

  **説明 :** イジング相互作用を記述するファイルを指定します。

- ``PairLift``

  **形式 :** str型 (デフォルトは "")

  **説明 :** ペアリフト相互作用を記述するファイルを指定します。

``file.output`` セクション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``path_to_output``

  **形式 :** str型 (デフォルトは "output")

  **説明 :** 出力ファイルを格納するディレクトリを指定します。

- ``energy``

  **形式 :** str型

  **説明 :** エネルギーを出力するファイル名を指定します。このキーワードがない場合には情報は出力されません。

- ``eigen``

  **形式 :** str型

  **説明 :** ハミルトニアンの固有値を出力するファイル名を指定します。このキーワードがない場合には情報は出力されません。

- ``green``

  **形式 :** str型

  **説明 :** 一体グリーン関数の出力ファイル名を指定します。このキーワードがない場合には情報は出力されません。

- ``initial``

  **形式 :** str型

  **説明 :** 初期状態読み込み用の一体グリーン関数の出力ファイル名を指定します。このキーワードがない場合には情報は出力されません。

- ``fij``

  **形式 :** str型

  **説明 :** ペア軌道因子fijの出力ファイル名を指定します。このキーワードがない場合には情報は出力されません。
