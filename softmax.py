import heapq as heapq


class Node:
    def __init__(self, wid, frequency):
        self.wid = wid
        self.frequency = frequency
        self.father = None
        self.is_left_child = None
        self.left_child = None
        self.right_child = None
        self.code = []
        self.path = []

    def __lt__(self,other):
        return self.wid < other.wid

class HuffmanTree:
    def __init__(self, word_frequency):
        self.word_count = len(word_frequency)          #有多少个单词
        self.nodes = []                              #保存huffman结点
        unmerged_node = []                             #构建huffman所用,保存(count, idx, 结点本身)
        word_frequency_list = []                       #只列出频数
        for index, value in word_frequency.items():
            word_frequency_list.append(value)


        for word_idx, count in word_frequency.items():
            node = Node(word_idx, count)
            unmerged_node.append((count, node))
            self.nodes.append(node)


        idx = len(self.nodes)                    #下一个结点的idx
        while len(unmerged_node) > 1:
            _, node1 = heapq.heappop(unmerged_node)
            _, node2 = heapq.heappop(unmerged_node)    #取出频率最小的两个结点
            new_node = Node(idx, node1.frequency + node2.frequency)   #huffman的新节点
            node1.father = new_node.wid
            node2.father = new_node.wid
            new_node.left_child = node1.wid
            node1.is_left_child = True
            new_node.right_child = node2.wid
            node2.is_left_child = False
            self.nodes.append(new_node)
            heapq.heappush(unmerged_node, (new_node.frequency, new_node))
            idx = len(self.nodes)

        self.get_huffman_code(unmerged_node[0][1].left_child)
        self.get_huffman_code(unmerged_node[0][1].right_child)



    def get_huffman_code(self, wid):
        print(wid)
        if self.nodes[wid].is_left_child:
            code = [1]
        else:
            code = [0]
        if self.nodes[wid].father is not None:
            self.nodes[wid].code = self.nodes[self.nodes[wid].father].code + code     #往左走是1，往右走是0
            self.nodes[wid].path = self.nodes[self.nodes[wid].father].path + [self.nodes[wid].father] #记录路径结点的wid


        if self.nodes[wid].left_child is not None:
            self.get_huffman_code(self.nodes[wid].left_child)
        if self.nodes[wid].right_child is not None:
            self.get_huffman_code(self.nodes[wid].right_child)


    def get_huffman_code_and_path(self):
        positive = []
        negative = []
        for wid in range(self.word_count):
            pos = []
            neg = []
            for i, code in enumerate(self.huffman[wid].code):
                if c == 1:
                    pos.append(self.huffman[wid].path[i])
                else:
                    neg.append(self.huffman[wid].path[i])
            positive.append(pos)     #positive[wid]就是到wid叶节点路径上向左的结点
            negative.append(neg)
        return positive, negative

