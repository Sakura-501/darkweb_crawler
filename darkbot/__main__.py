import argparse
import traceback

import httpx


from tools.config import config_all
from tools.tor_ip import get_tor_ip
from tools.url_parse import run_url
from first_websites_list import run_websites_list
from second_active_crawl import run_active_crawl
from third_search_keywords import search_one_keyword,search_keywords_from_config

config_all = config_all()
# tor代理设置
socks5h_proxy = "socks5://{}:{}".format(config_all.tor_proxy_ip, config_all.tor_proxy_port)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0"}


# sys.path.append(os.getcwd()+"/darkbot/tools")

def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="a bot for darkweb_crawler.")
    parser.add_argument("-u", "--url", type=str, help="Choose a url to crawl.")
    parser.add_argument("-w", "--websites_list", type=str, choices=["from_config"],
                        help="crawl websites from config.ini and get onion list.")
    parser.add_argument("-a", "--active_crawl", type=str, choices=["from_collection"],
                        help="active crawling for onion_url from mongodb_collection and get new onion domain.")
    parser.add_argument("-s", "--search_keywords", type=str,
                        help="search keywords([from_config] OR [the_keywords_you_input]) in https://ahmia.fi/ and get onion_url.")
    return parser


def all_run(args, client):
    # print(args)
    if args.url:
        run_url(client, args.url)
    elif args.websites_list == "from_config":
        run_websites_list(client)
    elif args.active_crawl == "from_collection":
        run_active_crawl(client)
    elif args.search_keywords is not None:
        if args.search_keywords == "from_config":
            search_keywords_from_config(client,config_all.third_search_keywords)
        else:
            search_one_keyword(client,args.search_keywords)
    else:
        args_parser.print_help()


if __name__ == "__main__":
    try:
        args_parser = get_argparse()
        args = args_parser.parse_args()
        # 检查是否存在tor代理，否则退出
        with httpx.Client(proxies=socks5h_proxy, timeout=15, headers=headers) as client:
            try:
                if get_tor_ip(client):
                    all_run(args, client)
            except Exception as e:
                traceback.print_exc()
                print("Please check your tor proxy OR other problems!!!")

    except KeyboardInterrupt:
        print("\nInterrupt received! Exit now!")
