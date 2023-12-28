import pymysql
from .config import config_all

config_all = config_all()

class mysql_latest:
    def __init__(self):
        self.db = pymysql.connect(host=config_all.mysql_host, port=config_all.mysql_port, user=config_all.mysql_user,
                                  password=config_all.mysql_password, database=config_all.mysql_database,
                                  charset=config_all.mysql_charset)
        self.cursor = self.db.cursor()
        self.create_title_body_table()

    def create_title_body_table(self):
        try:
            show_table_title_body_sql = "show tables like 'title_body'"
            self.cursor.execute(show_table_title_body_sql)
            if not self.cursor.fetchone():
                create_table_title_body_sql = """create table title_body(
                id int auto_increment primary key ,
                time_stamp timestamp default current_timestamp on update current_timestamp,
                url varchar(1024),
                title varchar(1024) ,
                body text
                )"""
                self.cursor.execute(create_table_title_body_sql)
            else:
                pass
        except Exception as e:
            print(e)
