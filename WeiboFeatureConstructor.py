# import chardet
class WeiboFeatureConstructor:
    db = None
    seg = None

    def __init__(self, db, seg):
        self.db = db
        self.seg = seg

    def getWeiboText(self):
        list = self.db.retrieve(3)
        file = open("retrieval.txt", "w+")
        for weibo in list:
            print(weibo["text"])
            # print(chardet.detect(weibo["text"]))
        file.close()
