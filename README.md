# 黑客社 Bot

> 用於 2019 社團博覽會

## bot簡介

+ 模擬Linux系統的指令，但為了安全，我們封鎖了一些可用指令
+ 另外你可以 cat 檔案(例如:新生茶會、facebook)以查看關於黑客社的額外資訊
+ 網站裡面還包含了一個找 Flag 的小遊戲

## 比較

相較於上一個版本，直接使用 python 執行指令，此版本是透過 javascript 模擬出類似 Linux 的環境

因為是透過 javascript 模擬，所以並不會發生 command injection 類似的攻擊情況發生

指令也不會輕易的被繞過，且跟 server 完全隔離，大幅的降低主機被攻擊的況狀產生

## 參考

[fake-terminal-website](https://github.com/luisbraganca/fake-terminal-website)
