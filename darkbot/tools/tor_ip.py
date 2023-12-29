import httpx
from bs4 import BeautifulSoup


def get_tor_ip(client: httpx.Client):
    check_ip_url="https://check.torproject.org"
    resp=client.get(check_ip_url)
    soup=BeautifulSoup(resp.text,"html.parser")
    div_content = soup.find("div", {"class": "content"})
    # 下面这个有点奇怪，浏览器看到的class是on。
    is_using_tor=div_content.find("h1",{"class":"on"})
    if not is_using_tor:
        raise Exception("Not using tor ip!!!")
    tor_ip=div_content.find("p")
    print(tor_ip.get_text().strip())
    return True
