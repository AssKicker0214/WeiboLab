# import chardet
class PhraseLevelSimilarityCalculator:
    def __init__(self, phrases_gen, finder):
        # f(ti)
        self.phrases = []
        self.articles_by_phrases = []
        self.phrase_occurrences = {}

        self.dice = []
        self.jcrd = []
        self.ovlp = []

        self.max_dice = None
        self.min_dice = None
        self.max_jcrd = None
        self.min_jcrd = None
        self.max_ovlp = None
        self.min_ovlp = None
        self.finder = finder

        self.occur(phrases_gen, True)
        self.co_occur()
        # for row in self.dice:
        #     print(row)
        # print()
        # for row in self.jcrd:
        #     print(row)
        # print()
        # for row in self.ovlp:
        #     print(row)

    # i < j
    def get_similarity(self, i, j, alpha=0.3, beta=0.3):
        wd = self.normalize(self.dice[i][j], self.min_dice, self.max_dice)
        wj = self.normalize(self.jcrd[i][j], self.min_jcrd, self.max_jcrd)
        wo = self.normalize(self.ovlp[i][j], self.min_ovlp, self.max_ovlp)
        similarity = alpha*wd + beta*wj + (1-alpha-beta)*wo
        return similarity


    def occur(self, phrases_gen, filter=False):
        for phrase in phrases_gen:
            if phrase not in self.phrase_occurrences:
                articles = self.finder.retrieve_by_word(phrase, 50)
                cnt = 0
                for article in articles:
                    cnt += article['abstract'].count(phrase)
                if filter and cnt == 0:
                    continue
                else:
                    self.phrase_occurrences[phrase] = cnt
                    self.phrases.append(phrase)
                    self.articles_by_phrases.append(articles)
        print(self.phrase_occurrences)

    def co_occur(self):
        length = len(self.phrases)
        self.dice = [[None for col in range(length)] for row in range(length)]
        self.jcrd = [[None for col in range(length)] for row in range(length)]
        self.ovlp = [[None for col in range(length)] for row in range(length)]
        for i in range(length):
            ti = self.phrases[i]
            articles_by_ti = self.articles_by_phrases[i]
            # ti's number by query of ti
            ti_by_ti = 0
            for article_by_ti in articles_by_ti:
                ti_by_ti += article_by_ti['abstract'].count(ti)

            for j in range(i + 1, length):
                tj = self.phrases[j]
                # print("ti,tj:", ti, tj)
                articles_by_tj = self.articles_by_phrases[j]

                # tj's number by query of tj
                tj_by_tj = 0
                for article_by_tj in articles_by_tj:
                    tj_by_tj += article_by_tj['abstract'].count(tj)

                # tj's number by query of ti
                tj_by_ti = 0
                for article_by_ti in articles_by_ti:
                    tj_by_ti += article_by_ti['abstract'].count(tj)

                # ti's number by query of tj
                ti_by_tj = 0
                for article_by_tj in articles_by_tj:
                    ti_by_tj += article_by_tj['abstract'].count(ti)

                # print(ti_by_ti, tj_by_tj, ti_by_tj, tj_by_ti)
                dice = self.wiki_dice(ti_by_ti, tj_by_tj, ti_by_tj, tj_by_ti)
                jcrd = self.wiki_jaccard(ti_by_ti, tj_by_tj, ti_by_tj, tj_by_ti)
                ovlp = self.wiki_overlap(ti_by_ti, tj_by_tj, ti_by_tj, tj_by_ti)

                self.dice[i][j] = dice
                self.jcrd[i][j] = jcrd
                self.ovlp[i][j] = ovlp

    def wiki_dice(self, x, y, x_by_y, y_by_x):
        if x == 0 or y == 0:
            return 0
        rs = 0
        if x_by_y == 0 or y_by_x == 0:
            rs = 0
        else:
            rs = (0.0 + x_by_y + y_by_x) / (x + y)

        # update max / min
        if self.max_dice is None or self.max_dice < rs:
            self.max_dice = rs

        if self.min_dice is None or self.min_dice > rs:
            self.min_dice = rs

        return rs

    def wiki_jaccard(self, x, y, x_by_y, y_by_x):
        if x == 0 or y == 0:
            return 0
        rs = min(x_by_y, y_by_x) / (x + y + 0.0 - max(x_by_y, y_by_x))

        # update max / min
        if self.max_jcrd is None or self.max_jcrd < rs:
            self.max_jcrd = rs

        if self.min_jcrd is None or self.min_jcrd > rs:
            self.min_jcrd = rs
        return rs

    def wiki_overlap(self, x, y, x_by_y, y_by_x):
        if x == 0 or y == 0:
            return 0
        rs = (min(x_by_y, y_by_x) + 0.0) / min(x, y)

        # update max / min
        if self.max_ovlp is None or self.max_ovlp < rs:
            self.max_ovlp = rs

        if self.min_ovlp is None or self.min_ovlp > rs:
            self.min_ovlp = rs

        return rs

    # map to value from 0 to 1
    def normalize(self, x, min, max):
        return (x - min + 0.0)/(max - min)

    def remove_semantic_duplicate(self):
        length = len(self.jcrd)
        max = 0
        most_duplicated_phrase = None
        for i in range(length):
            sum_of_similarity = 0
            for j in range(length):
                if i<j:
                    sum_of_similarity += self.get_similarity(i, j)
                elif i>j:
                    sum_of_similarity += self.get_similarity(j, i)

            if sum_of_similarity > max:
                most_duplicated_phrase = self.phrases[i]
                max = sum_of_similarity
        if most_duplicated_phrase is not None:
            for seed_phrase in self.phrases:
                if seed_phrase != most_duplicated_phrase:
                    yield seed_phrase


class WeiboFeatureConstructor:
    db = None
    finder = None
    seg = None

    def __init__(self, db, finder, seg):
        self.db = db
        self.seg = seg
        self.finder = finder

    def get_weibo_text(self):
        list = self.db.retrieve(3)
        for weibo in list:
            print("======= weibo ===========")
            text = weibo['text']
            sentences = self.seg.sentence_segment(text)
            for sentence in sentences:
                print("------sentence------")
                print(sentence)
                words_gen = self.seg.phrase_segment(sentence)
                phrase_feature = PhraseLevelSimilarityCalculator(words_gen, self.finder)
                # similarity = phrase_feature.get_similarity()
                words_gen = None

    def get_weibo_text_mock(self):
        resource = None
        for weibo in resource:
            for sentences in weibo:
                # build sentence level feature and phrase level feature
                for sentence in sentences:
                    sentence_level_seeds = sentence.phrases
                    phrase_feature = PhraseLevelSimilarityCalculator(sentence_level_seeds, self.finder)
                    phrase_level_seeds = phrase_feature.remove_semantic_duplicate()

    def wiki_query(self, seed_phrase, query_type):
        words_gen = self.seg.word_segment(seed_phrase)
        raw_semantic_features = self.db.multi_words_query(words_gen, query_type)