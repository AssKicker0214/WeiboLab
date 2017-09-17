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
            sentences = self.seg.sentence_segment(text)
            for sentence in sentences:
                words_gen = self.seg.phrase_segment(sentence)


