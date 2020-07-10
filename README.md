# nab

「統計分析」工具包

## 安裝

請先安裝 python 3，並：

    git clone https://github.com/family97109/nab.git

## 設定環境

使用 [pip](https://pip.pypa.io/en/stable/) 設定環境，此步驟會安裝相關 package

Windows

    pip install --editable .

Mac

    pip3 install --editable .

## 功能列表

### login_count

* 功能：獲取登入總數

* 參數：
  * MySQL
    * dev
    * testDB
  * DB name
  * Time
    * N：前幾個月
    * yyyy-mm-dd：指定日期
  * User
    * admin
    * member
    * reseller
  * Plot

### user_agent_os_browser

* 功能：獲取 os, browser 登入資訊

* 參數：
  * MySQL
    * dev
    * testDB
  * DB name
  * Time
    * N：前幾個月
    * yyyy-mm-dd：指定日期
  * User
    * admin
    * member
    * reseller
  * Info
    * os：只獲取 os 資料
    * browser：只獲取 browser 資料
    * both：同時獲取 os, browser 資料
  * Plot
  