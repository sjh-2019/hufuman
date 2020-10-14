class HuffNode():
    '''虚类，检查是否为叶节点以及获取权重'''
    def get_weight(self):
        raise NotImplementedError("The Node doesn't define 'get_weight'")
    def isleaf(self):
        raise NotImplementedError("the Node doesn't define 'isleaf'")


class LeafNode(HuffNode):
    '''叶节点'''
    def __init__(self,value=0,freq=0):
        super(LeafNode,self).__init__()
        self.value=value
        self.weight=freq

    def isleaf(self):
        return True

    def get_weight(self):
        return self.weight

    def get_value(self):
        return self.value


class IntlNode(HuffNode):
    '''中间节点'''
    def __init__(self,left_child=None,right_chid=None):
        super(IntlNode,self).__init__()
        # 概率相加
        self.weight=left_child.weight+right_chid.weight
        self.left_child=left_child
        self.right_child=right_chid

    def isleaf(self):
        return False

    def get_weight(self):
        return self.weight

    def get_left(self):
        return self.left_child

    def get_right(self):
        return self.right_child


class HuffTree():
    def __init__(self,flag,value=0,freq=0,left_tree=None,right_tree=None):
        if flag==0:
            self.root=LeafNode(value,freq)
        else:
            self.root=IntlNode(left_tree.root,right_tree.root)

    def get_weigt(self):
        return self.root.get_weight()

    def traverse_huffman_tree(self,root,code,char_freq):
        '''递归遍历哈夫曼树，得到最优码，将最有码保存在字典char_freq中。'''
        if root.isleaf():
            char_freq[root.get_value()]=code
            return None
        else:
            self.traverse_huffman_tree(root.get_left(),code+'0',char_freq)
            self.traverse_huffman_tree(root.get_right(), code + '1', char_freq)


def buildHuffmanTree(list_hufftrees):
    '''构造哈夫曼树'''