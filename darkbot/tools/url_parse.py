from bs4 import BeautifulSoup
from .create_mysql import mysql_latest
import datetime


def insert_title_body_to_table(args_url,title,body):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_title_body_sql="insert into title_body(time_stamp,url,title,body) values(%s,%s,%s,%s)"

    mysql_instance = mysql_latest()
    db = mysql_instance.db
    cursor = mysql_instance.cursor
    try:
        cursor.execute(insert_title_body_sql,(current_time,args_url,title,body))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

def run_url(client,args_url):
    resp=client.get(url=args_url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text,"html.parser")
        title=soup.title.string.strip()
        print("title: \n"+title)
        body=soup.find("body").get_text().strip()
        print("body: \n"+body)
        # print(args_url+": insert_title_body_to_table")
        # insert_title_body_to_table(args_url,title,body)


# T