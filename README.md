# Spider program for estate

- A spider engine for estate website. 
- Crawling the price data and other infomation into mysql.
- Analyze the data in mysql.

### Support estate websites:
- Lianjia: `https://sh.lianjia.com`

### Spider library support
- Library: `scrapy`
- URL: https://www.osgeo.cn/scrapy/intro/tutorial.html

## Install
```bash
$ pip install virtualenv
$ virtualenv .virtualenv -p /usr/bin/python3
$ sudo curl -kL "https://raw.githubusercontent.com/erning/ve/master/ve" -o "/usr/local/bin/ve"
$ sudo chmod +x /usr/local/bin/ve
$ ve pip install -r requirements.txt
```
- Make sure the configuration of mysql (`ESTATE_DB_CONNECTION_CONFIG`) point to the database server.

## Commands:
Work folder:            cd ./estate
- For help:               `ve scrapy -h`
- Create tables in mysql: `ve scrapy create_tables` 
- Drop tables in mysql:   `ve scrapy drop_tables`

## Run & Test a spider
Work folder:		cd ./estate
- `ve scrapy crawl property (spider name)`

Created by : barry
