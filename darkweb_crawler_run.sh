#!/bin/bash
echo "Stop last darkweb_crawler_run.sh first, Please wait for a moment!"
#pkill -f "darkweb_crawler_run.sh"
while [ 1 ]; do
    #nohup command > output.log 2>&1 &
    echo "1. 从config.ini获取暗网索引网站/github等网站获取onion域名。"
    python3 darkbot -w from_config
    sleep 5;
    echo "2. 在https://ahmia.fi/搜索来自config.ini的关键字，在结果中匹配出onion域名。"
    python3 darkbot -s from_config
    sleep 5;
    echo "3. 基于tor2web项目，在google/duckduckgo/bing三大搜索引擎使用site方式搜索onion域名。"
    python3 darkbot -t from_config
    sleep 5;
    echo "4. 从数据库中查询出上述onion域名，进一步主动访问爬取更多的onion域名。"
    python3 darkbot -a from_collection
    sleep 5;
done