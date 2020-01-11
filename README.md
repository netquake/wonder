# Spider program for estate

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

## Commands:
For help:               `ve scrapy -h`
Create tables in mysql: `ve scrapy create_tables` 
Drop tables in mysql:   `ve scrapy drop_tables`

## Run & Test a spider
`ve scrapy crawl property (spider name)`

