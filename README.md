# darkweb_crawler(darkbot)
## 五种onion域名收集方式
1. 基于暗网索引网站/github等网站获取onion域名(待完成)
2. 基于torweb的搜索引擎获取onion域名(待完成)
3. 基于爬虫解析页面主动获取onion域名(待完成)
4. 基于Telegram/Twitter等交流工具获取onion域名(待完成)
5. 基于部署具有hsdir(隐藏服务节点)标签的节点获取onion域名(待完成)

## darkweb_crawler数据库设计
### onion_list集合
#### 一、基于暗网索引网站/github等网站获取onion域名
1. 暗网索引网站/github：

| _id | source | url  | is_crawl | title | head | body |
|-----|------|------|----------|-------|------|------|
| xxx | 索引网站 | 索引网站 | 1        | xxx   | xxx  | xxx  |

2. 爬取暗网索引网站/github时(第三种收集方式同理于此)，获取到url插入集合中

| _id | source | url  | is_crawl | title | head | body |
|-----|------|------|----------|-------|------|------|
| xxx | 来源网站 | 当前网站 | 0        | None  | None | None |

3. 从表获取到未爬url,爬取完后更新集合内容

| _id | source | url  | is_crawl | title | head | body |
|-----|--------|------|----------|-------|------|------|
| xxx | 来源索引网站 | 当前网站 | 1        | xxx   | xxx  | xxx  |

## 使用前配置
### tor网络
[安装参考网址，先看这个！！！](https://hanblog.fun/2021/04/07/2021-4-7-tor-simple-configer/)
```shell
brew install tor

To start tor now and restart at login:
  brew services start tor
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/tor/bin/tor

# 配置文件在：
cd /opt/homebrew/etc/tor

# 命令行使用：
export all_proxy=socks5h://127.0.0.1:9050
或者直接启动挂在后台
tor
```