.. highlight:: none

.. _Subsec:initial:

Initial指定ファイル
~~~~~~~~~~~~~~~~~~~~

グリーン関数 :math:`G_{ij\sigma_1\sigma_2}\equiv \langle c_{i\sigma_1}^\dagger c_{j\sigma_2}\rangle` の初期値を与えます。
ファイル形式は出力ファイルの ``green`` ファイルと同じです。
なお、値を指定しないグリーン関数の要素には0が入ります。
以下にファイル例を記載します。

::

    0 0 0 0  0.9517526553947047  0.0
    0 0 1 0 -0.03971951040016314 0.0
    0 0 2 0  0.09202884754223833 0.0
    0 0 3 0 -0.039719448981075135 0.0
    0 0 4 0  0.09202884754219534 0.0
    0 0 5 0 -0.03971947216145664 0.0
    0 0 6 0  0.09202884753253462 0.0
    0 0 7 0  0.09202884754259735 0.0
    0 1 0 1  0.04824734460529617 0.0
    0 1 1 1  0.03971951040016307 0.0
    …

ファイル形式
^^^^^^^^^^^^

-  ``[i] [s1] [j] [s2]  [v.real] [v.imag]``

パラメータ
^^^^^^^^^^

-  ``[i]``, ``[j]``

   **形式 :** int型

   **説明 :**
   サイト番号を指定する整数。\ ``[i]``\ が\ :math:`i`\ サイト、\ ``[j]``\ が\ :math:`j`\ サイトを表します。

-  ``[s1]``, ``[s2]``

   **形式 :** int型

   **説明 :**
   スピンを指定する整数。\ ``[s1]``\ が\ :math:`\sigma_1`\ 、\ ``[s2]``\ が\ :math:`\sigma_2`\ に対応します。
   0=アップスピン, 1=ダウンスピン を表します。

-  ``[v.real]``, ``[v.imag]``

   **形式 :** float型

   **説明 :**
   :math:`\langle c_{i\sigma_1}^{\dagger}c_{j\sigma_2}\rangle`\ の値を表します。
   ``[v.real]``\ が実部、\ ``[v.imag]``\ が虚部を表します。

.. raw:: latex

   \newpage
