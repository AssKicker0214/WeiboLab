import pymysql


class DataConnector:
    def getCnct(self, dbname):
        config = {
            'host': '127.0.0.1',
            # 'host': '192.168.0.100',
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


class WeiboConnector(DataConnector):
    # cnct = None

    def __init__(self):
        self.cnct = self.getCnct("sina_weibo")

    def retrieve(self, size=None):
        cursor = self.cnct.cursor()
        query = '''
            select * from optimized_weibo limit 20, 60;
        '''
        cursor.execute(query)
        if size is None:
            result = cursor.fetchall()
        else:
            result = cursor.fetchmany(size)
        cursor.close()
        return result

    def retrieve_mock(self):
        return ''


class WikiConnector(DataConnector):
    # cnct = None

    def __init__(self):
        self.cnct = self.getCnct("wikipedia")

    def insertWikiDoc(self, doc):
        cursor = self.cnct.cursor()
        query = '''
            INSERT INTO docs_full_size (`title`, `abstract`, `url`)
            VALUES ("%s", "%s", "%s");
        '''
        try:
            cursor.execute(query % (doc["title"] + "", doc["abstract"] + "", doc["url"] + ""))
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
        cursor.execute("DELETE FROM docs_full_size")
        self.cnct.commit()

    def retrieve_by_word(self, word, top_C=50):
        cursor = self.cnct.cursor()
        query = '''
            SELECT title, abstract from docs_full_size WHERE MATCH(abstract) AGAINST('%s') LIMIT %d;
        '''
        cursor.execute(query % (word, top_C))
        self.cnct.commit()
        result = cursor.fetchall()
        cursor.close()
        return result

    def multi_words_query(self, words, query_type, top_w=100):
        query_conditions = []
        for word in words:
            query_conditions.append(" match(abstract) against('%s') " % word)
        condition = query_type.join(query_conditions)
        query = "SELECT title FROM docs_full_size WHERE"+condition+"LIMIT "+str(top_w)
        # print("=>",query)
        cursor = self.cnct.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
# wiki = WikiConnector()
# rs = wiki.retrieve_by_word('数学', 10)
# for t in rs:
#     print(t)
#     print("=====================",t['abstract'].count('数学'))
