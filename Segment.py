import jieba
import jieba.posseg as pos_seg
import re


class Segment:
    def __init__(self):
        jieba.load_userdict("./data/dict.txt")
        pass

    def sentence_segment(self, text):
        sentences = re.split('[。!！？?]+', text)
        return sentences

    def phrase_segment(self, sentence):
        words_gen = jieba.cut(sentence)
        return words_gen

    def word_segment(self, phrase):
        words_gen = jieba.cut(phrase)
        return words_gen

    def term_segment(self, phrase):
        words = pos_seg.cut(phrase)
        for w, t in words:
            if "n" in t:
                yield w
    # def phrase_segment_mock(self):

    def segment(self, text, sentence=True, phrase=True):
        pass

# seg = Segment()
# seg.term_segment("欧冠与热刺的比赛")