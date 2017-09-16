import pymysql


class DataConnector:
    def getCnct(self, dbname):
        config = {
            # 'host': '127.0.0.1',
            'host': '192.168.0.100',
            'port': 3306,
            'user': 'root',
            'password': 'test',
            'db': dbname,
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }
        cnct = pymysql.connect(**config)

        # 使用 utf-8
        cnct.cursor().execute("SET NAMES utf8")
        return cnct


'''
'host': '127.0.0.1',
          'port': 3306,
          'user': 'root',
          'password': 'zhyea.com',
          'db': 'employees',
          'charset': 'utf8mb4',
          'cursorclass': pymysql.cursors.DictCursor
'''


class WeiboConnector(DataConnector):
    cnct = None

    def __init__(self):
        self.cnct = self.getCnct("sina_weibo")

    def retrieve(self, size=None):
        cursor = self.cnct.cursor()
        query = '''
            select * from optimized_weibo;
        '''
        cursor.execute(query)
        if size is None:
            result = cursor.fetchall()
        else:
            result = cursor.fetchmany(size)
        return result


class WikiConnector(DataConnector):
    cnct = None

    def __init__(self):
        self.cnct = self.getCnct("wikipedia")

    def insertWikiDoc(self, doc):
        cursor = self.cnct.cursor()
        query = '''
            INSERT INTO docs (`title`, `abstract`, `url`)
            VALUES ("%s", "%s", "%s");
        '''
        try:
            cursor.execute(query % (doc["title"]+"", doc["abstract"]+"", doc["url"]+""))
            self.cnct.commit()
        except Exception:
            print("error=>", doc)
            return True
        else:
            return True
        finally:
            cursor.close()

    def removeDocs(self):
        cursor = self.cnct.cursor()
        cursor.execute("DELETE FROM docs")
        self.cnct.commit()