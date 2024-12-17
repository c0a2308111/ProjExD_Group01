# KOKATONTALE

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
* 大学を卒業するために、単位をめぐって教授と激しい戦いをするこうかとん（主人公一年生）、ステージは1年生、２年生、３年生、4年生の順にレベルが上がる。


## ゲームの遊び方
* 「W」「A」「S」「D」の4つのキーを用いてこうかとんを操作します。攻撃はターン制で相手とプレイヤーで交互に攻撃をします。
* こうかとんのHPが0になったらラウンドを一個前にもとし、こうかとんのHPが4回0になったらゲームオーバーとなる。

## ゲームの実装
### 共通基本機能
* 背景画像と主人公キャラクター、敵キャラ、攻撃エフェクトを描画

### 分担追加機能
* こうかとんの操作、こうかとんのエフェクト（担当：）：上記で述べた4つのキーを用いてこうかとんを操作できる機能、こうかとんの攻撃エフェクト機能

* 敵キャラの攻撃エフェクト（担当：）：敵キャラが攻撃をする機能

* 獲得単位、こうかとんのHP表示（担当：）：各ラウンドで得た単位数（スコア）とこうかとんのHPを計算する機能

* 回復アイテム（担当:）:使用するとこうかとんのHPを一定数回復できる機能

* ドロップアイテム管理（担当：）：敵を倒したらランダムでアイテムをドロップする機能 

### ToDo
- [ ] プログラムの骨組みの作成
- [ ] 関数名の統一

### メモ

