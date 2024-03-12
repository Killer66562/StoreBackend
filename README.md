# 購物網站後端

## 專案啟動方式
1. 下載python (3.10 or 3.11 only, 3.12 May cause bugs)
2. pip install virtualenv (安裝虛擬環境套件)
3. 下載本專案
4. 進到專案根目錄並開啟終端機 (cmd, powershell, ...)
5. 終端機輸入 "python -m venv venv" 建立虛擬環境
6. 啟用虛擬環境 (這個自己查，Win, Mac, Linux好像都不太一樣)
7. 確認虛擬環境已啟用 (有(venv)字樣) 並輸入 "pip instll -r requirements.txt" 安裝所需套件
8. 進到 ./src 目錄
9. 輸入 "alembic upgrade head" 初始化資料庫 (測試環境使用sqlite3)
10. 輸入 "python main.py" 啟動專案

## 待辦事項
+ 構想API端點路徑
+ 確認是否有需要新增的Model
+ 實作所有API端點

## Branch lock test