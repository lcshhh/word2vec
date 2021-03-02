from data_process import Dataset
import numpy
from model import skip_gram
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.optim as optim


def word2vec(input_file_name,
                 output_file_name,
                 emb_dimension=100,
                 batch_size=100000,
                 window_size=5,
                 iteration=5,
                 using_hs=False,
                 using_neg=False,
                 context_size=2,
                  ):
    dataset = Dataset(input_file_name)
    optimizer = optim.SGD(self.skip_gram_model.parameters(), lr=0.01)
    pair_count = dataset.pair_count(self.window_size)
    batch_count = iteration * pair_count / batch_size
    skip_gram_model = skip_gram(self.emb_size, self.emb_dimension)
    skip_gram_model.save_embedding(self.data.idx2word, 'skip_gram_begin_embedding.txt')
    for i in range(batch_count):
        word_pairs = self.data.get_batch_pairs(self.batch_size, self.window_size)
        if self.using_hs:
            pos_pairs, neg_pairs = self.data.get_pairs_by_hs(word_pairs)
        else:
            pos_pairs, neg_pairs = self.data.get_pairs_by_neg_sampling(pos_pairs, 5)

        pos_u = [int(pair[0]) for pair in pos_pairs]
        pos_v = [int(pair[1]) for pair in pos_pairs]
        neg_u = [int(pair[0]) for pair in neg_pairs]
        neg_v = [int(pair[1]) for pair in neg_pairs]

        self.optimizer.zero_grad()
        loss = self.skip_gram_model.forward(pos_u, pos_v, neg_u, neg_v)
        loss.backward()
        self.optimizer.step()

    self.skip_gram_model.save_embedding(self.data.idx2word, self.output_file_name)



if __name__ == '__main__':
    input_file_name = "./test.txt"
    output_file_name = "./output.txt"
    skip_gram = True
    #using_neg = True
    using_hs = True
    word2vec(input_file_name=input_file_name,
                        output_file_name=output_file_name,
                        context_size=2,
                        using_hs=using_hs)