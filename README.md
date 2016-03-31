本意要做一个宏观金融数据平台，定期抓取相关的金融数据，现仅完成了一些基本模块
服务想布在openshift上，但奈何国内访问速度太慢。

crawl_yahoo.py：用于抓取yahoo财经网站上的股票日线数据。
financecrawl: 下面有几个爬虫。
dataModels.py: 数据结构定义。

# crawl_yahoo.py的用法

用于抓取Yahoo财经的沪深两市股票日线数据，可以将抓取的数据存储成pickle文件，也可以将其存入数据库，如果是存储到数据库的话设置OPENSHIFT_POSTGRESQL_DB_URLG环境变量为sqlalchemy数据库URL，数据模型用dataModels.py。用法如下：
## 抓取到文件
``` python
if __name__ == '__main__':
    
    # 在$OPENSHIFT_DATA_DIR/stocks.txt文件中存储要抓取的股票列表
    crawler = YahooCrawler(stockfile=os.path.join(os.environ['OPENSHIFT_DATA_DIR'],
        'stocks.txt'))
    # Yahoo只能抓取前一天的数据，将start最晚改为昨天，也可以改为更靠前的日子
    start = yestoday()
    crawler.run(start=start)
    
    filename = start.strftime('%Y%m%d') + '.pkl'
    
    crawler.save2pickle(filename)
```
## 抓取到数据库
``` python
if __name__ == '__main__':
    # 抓取到数据库时股票列表是从数据库中读取，开始时间
    # 也是从数据库中读出每支要抓取的股票数据的最晚日期
    crawler = YahooCrawler(db_enabled=True)
    crawler.run()
    crawler.save2database(self.crawled_data)
```

## 从文件中读取到数据库
``` python
from crawl_yahoo import YahooCrawler

if __name__ == '__main__':
    import pandas as pd
    data = pd.read_pickle('filename.pkl')
    YahooCrawler.save2database(data)

```

    

