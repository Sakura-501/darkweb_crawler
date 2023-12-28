import argparse

import httpx

from tools.config import config_all
from tools.tor_ip import get_tor_ip
from tools.url_parse import run_url
from first_websites_list.onion_crawler import run_websites_list

config_all=config_all()
# tor代理设置
socks5h_proxy="socks5://{}:{}".format(config_all.tor_proxy_ip,config_all.tor_proxy_port)


def get_argparse()-> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="a bot for darkweb_crawler.")
    parser.add_argument("-u","--url",type=str,help="Choose a url to crawl.")
    parser.add_argument("-w","--websites_list",type=str,choices=["config"],help="crawl websites from config.ini and get onion list.")
    return parser

def all_run(args,client):
    # print(args)
    if args.url:
        run_url(client,args.url)
    elif args.websites_list == "config":
        run_websites_list()


if __name__ == "__main__":
    try:
        args_parser=get_argparse()
        args=args_parser.parse_args()
        # 检查是否存在tor代理，否则退出
        with httpx.Client(proxies=socks5h_proxy, timeout=10) as client:
            try:
                 if get_tor_ip(client):
                    all_run(args,client)
            except Exception as e:
                print(e)
                print("Please check your tor proxy!!!")

    except KeyboardInterrupt:
        print("\nInterrupt received! Exit now!")