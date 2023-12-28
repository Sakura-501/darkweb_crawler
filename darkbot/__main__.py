import argparse

import httpx

from tools.config import config_all
from tools.tor_ip import get_tor_ip
from tools.url_parse import run_url

config_all=config_all()



def get_argparse()-> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="a bot for darkweb_crawler.")
    parser.add_argument("-u","--url",type=str,help="Choose a url to crawl.")
    parser.add_argument("-w","--websites_list",type=str,choices=["config"],help="crawl websites from config.ini and get onion list.")
    return parser

def all_run(args):
    # tor代理设置
    socks5h_proxy="socks5://{}:{}".format(config_all.tor_proxy_ip,config_all.tor_proxy_port)
    # print(args)
    if args.url:
        with httpx.Client(proxies=socks5h_proxy,timeout=10) as client:
            # 检查是否为tor代理
            if get_tor_ip(client):
                run_url(client,args.url)
    elif args.websites_list == "config":
        print("config")


if __name__ == "__main__":
    try:
        args_parser=get_argparse()
        args=args_parser.parse_args()
        all_run(args)
    except KeyboardInterrupt:
        print("\nInterrupt received! Exit now!")