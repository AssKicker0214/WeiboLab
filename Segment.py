import jieba
import jieba.posseg as pos_seg
import re


class Segment:
    def __init__(self):
        pass

    def sentence_segment(self, text):
        sentences = re.split('[。!！？?]+', text)
        return sentences

    def phrase_segment(self, sentence):
        words_gen = jieba.cut(sentence)
        return words_gen

    def segment(self, text, sentence=True, phrase=True):
        pass

