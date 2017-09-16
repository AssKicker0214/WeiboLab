import xml.sax


class WikiHandler(xml.sax.ContentHandler):
    __type = ''
    __content = ''
    __doc = {}
    db = None
    def __init__(self, dbConnector):
        self.currentData = ""
        self.db = dbConnector

    def startDocument(self):
        print("开始解析xml文档...")
        print("清除数据库原有数据")
        self.db.removeDocs()

    def startElement(self, name, attrs):
        self.__type = name
        pass

    def characters(self, content):
        if self.__type == 'title':
            self.__doc["title"] = content
        elif self.__type == 'abstract':
            self.__doc["abstract"] = content
        elif self.__type == 'url':
            self.__doc["url"] = content

        self.__type = ''

    def endElement(self, name):
        if name == 'doc':
            # 一个文档解析完毕
            # print(self.__doc)
            if self.db.insertWikiDoc(self.__doc):
                self.__doc = {}
            else:
                raise InsertIntoDatabaseError()
            # raise TestOverError()





def get_parser():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    return parser


class TestOverError(Exception):
    def __init__(self):
        Exception("test over")

class InsertIntoDatabaseError(Exception):
    def __init__(self, doc):
        Exception("error happens when insertInto database")