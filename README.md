# WeiboLab
*created by QiaoHongbo* 

Data mining for short textual data in social media.

## Data Source
### Semantic Knowledge Source
Wikipedia of xml format can be downloaded [here](https://dumps.wikimedia.org/zhwiki/latest/). We use the *latest-abstract* which contains only title, abstract and links of a wikipedia page.
A preprocessing work is required before drop it into database. So We provide a quick sax parsing and dirty data cleaning.
### Social Media text
We choose textual data from different users of sina weibo. As it is a pretty hard work to crawl data from sina, (considering of the more and more strong anti-crawler technology has been put into use), we in hence download some data from [csdn](http://download.csdn.net/download/u012721450/6511879). The data is old but sufficient for us. But we won't use it this time.

Here's my environment,

`Python 3.6` `Anaconda 3` `MySQL 5.7`

The environment is important, because some of the features I use only supported by the latest version.
