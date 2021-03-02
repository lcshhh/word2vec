import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class skip_gram(nn.Module):
    def __init__(self, emb_size, emb_dimension):
        super(skip_gram, self).__init__()
        self.emb_size = emb_size
        self.emb_dimension = emb_dimension
        self.u_embeddings = nn.Embedding(emb_size, emb_dimension, sparse=True)
        self.v_embeddings = nn.Embedding(2 * emb_size - 1, emb_dimension, sparse=True)
        initrange = 0.5 / self.emb_dimension
        self.u_embeddings.weight.data.uniform_(-initrange, initrange)
        self.v_embeddings.weight.data.uniform_(-0, 0)

    def forward(self, pos_u, pos_v, neg_u, neg_v):
        losses = []
        pos_u = self.u_embeddings(Variable(torch.LongTensor(pos_u)))
        pos_v = self.v_embeddings(Variable(torch.LongTensor(pos_v)))
        pos_score = torch.mul(pos_u, pos_v)
        pos_score = torch.sum(score, dim=1)
        pos_score = F.logsigmoid(pos_score)
        losses.append(sum(score))
        neg_u = self.u_embeddings(Variable(torch.LongTensor(neg_u)))
        neg_v = self.v_embeddings(Variable(torch.LongTensor(neg_v)))
        neg_score = torch.mul(neg_u, neg_v)
        neg_score = torch.sum(neg_score, dim=1)
        neg_score = F.logsigmoid(-1 * neg_score)
        losses.append(sum(neg_score))
        return -1 * sum(losses)

    def save_embedding(self, id2word, file_name):
        embedding = self.u_embeddings.weight.data.numpy()
        fout = open(file_name, 'w', encoding="UTF-8")
        fout.write('%d %d\n' % (len(id2word), self.emb_dimension))
        for wid, w in id2word.items():
            e = embedding[wid]
            e = ' '.join(map(lambda x: str(x), e))
            fout.write('%s %s\n' % (w, e))