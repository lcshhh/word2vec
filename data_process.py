import numpy
from softmax import HuffmanTree


class Dataset:
    def __init__(self, file_name):
        self.get_words(file_name)
        tree = HuffmanTree(self.word_frequency)
        self.huffman_positive, self.huffman_negative = tree.get_huffman_code_and_path()
        self.input_file_name = file_name
        self.input_file = open(self.input_file_name, encoding="UTF-8")
        self.text_size = 0            #单词的个数
        self.sentence_count = 0       #句子的个数
        word_frequency = dict()       #word:count
        for line in self.input_file:
            self.sentence_count += 1
            line = line.strip().split(' ')
            self.text_size += len(line)
            for w in line:
                word_frequency[w] = word_frequency[w] + 1 if w in word_frequency else 1
        self.word2idx = dict()       #单词和索引的互相映射
        self.idx2word = dict()
        word_idx = 0
        self.word_frequency = dict()
        for w, count in sorted(word_frequency.items(), key = lambda value:(value[1], value[0])):   #按照频率从小到大排序
            self.word2idx[w] = word_idx
            self.idx2word[word_idx] = w
            self.word_frequency[word_idx] = count
            word_idx += 1
        self.word_count = len(self.word2idx)    #单词的个数



    def get_batch_pairs(self, batch_size, window_size):
        batch_pairs = []
        while len(batch_pairs) < batch_size:
            for _ in range(self.sentence_count):
                sentence = self.input_file.readline()
                if sentence is None or sentence == '':
                    self.input_file = open(self.input_file_name, encoding="utf-8")
                    sentence = self.input_file.readline()
                word_ids = []
                for word in sentence.strip().split(' '):
                    word_ids.append(self.word2idx[word])
                for idx1, center_word in enumerate(word_ids):
                    for idx2, context in enumerate(word_ids[max(idx1 - window_size, 0):min(idx2 + window_size + 1, len(word_ids))]):
                        if idx1 != idx2:
                            batch_pairs.append((center_word, context))
        return batch_pairs



    def get_pairs_by_neg_sampling(self, pos_word_pair, count):
        sample_table = []
        sample_table_size = 1e8
        frequency_array = numpy.array(list(self.word_frequency.values()))
        frequency_sum = sum(frequency_array)
        ratio_array = frequency_array / frequency_sum
        ratio_array = ratio_array ** 0.75
        neg_word_pair = []
        for pair in pos_word_pair:
            neg_v = torch.multinomial(ratio_array, count, True)
            neg_word_pair += zip([pair[0]] * count, neg_v)
        return pos_word_pair, neg_word_pair


    def get_pairs_by_hs(self, word_pair):
        pos_word_pair = []
        neg_word_pair = []
        a = len(self.word2idx) - 1
        for i in range(len(word_pair)):
            pair = word_pair[i]
            pos_word_pair += zip([pair[0]] *
                                 len(self.huffman_positive[pair[1]]),
                                 self.huffman_positive[pair[1]])
            neg_word_pair += zip([pair[0]] *
                                 len(self.huffman_negative[pair[1]]),
                                 self.huffman_negative[pair[1]])

        return pos_word_pair, neg_word_pair


    def pair_count(self, window_size):
        return self.sentence_length * (2 * window_size - 1) - (
            self.sentence_count - 1) * (1 + window_size) * window_size

