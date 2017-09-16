import jieba
import re


class Segment:
    def __init__(self):
        pass

    def sentence_segment(self, text):
        pass

    def phrase_segment(self):
        pass

    def segment(self, text, sentence=True, phrase=True):
        sentences = re.split('[。!！？?]+', text)
        rs = {"sentence": sentences, "phrases": []}
        if phrase:
            for s in sentences:
                rs["phrases"].append(jieba.cut(s))
        return rs

print(jieba.cut("你的眼睛发着光"))