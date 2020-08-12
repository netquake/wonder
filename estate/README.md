# Spiders

 - juwai_spiders/spider/propertyguru_agents:
 
    - It's a manually Spider for scraping data from `www.propertyguru.com.sg`
    
    - Support data cache data with temp storage.
    
    - Save data into sqlite3 at path `~/agents.db`
    
    - Spider will halt and wait for retrying after get forbidden.


### Installation

 - `propertyguru_agents`'s dependent libraries :
    - Python==3.6
    - Scrapy==2.2.1
    - pychrome==0.2.3       (conflicts with file requirements.txt)
    - SQLAlchemy==1.3.3
    - git+ssh://git@github.com/juwai/python-config.git@master#egg=juwai_config
    - git+ssh://git@github.com/juwai/python-logging.git@master#egg=juwai_logging
    - zerorpc==0.6.1

```bash
$ virtualenv .virtualenv -p /usr/local/bin/python3.6
$ ve pip install dependent libraries.
```


### Running commands:

 - propertyguru_agents:
    - cd src/jw/scripts/spiders
    - ve scrapy crawl propertyguru_agents
