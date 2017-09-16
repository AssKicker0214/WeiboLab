# import chardet
class WeiboFeatureConstructor:
    db = None
    seg = None

    def __init__(self, db, seg):
        self.db = db
        self.seg = seg

    def getWeiboText(self):
        list = self.db.retrieve(3)
        for weibo in list:
            text = weibo['text']
            seg_result = self.seg.segment(text)
            print(seg_result)


