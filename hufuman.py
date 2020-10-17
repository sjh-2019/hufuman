import six


class HuffNode():
    '''虚类，检查是否为叶节点以及获取权重'''

    def get_weight(self):
        raise NotImplementedError("The Node doesn't define 'get_weight'")

    def isleaf(self):
        raise NotImplementedError("the Node doesn't define 'isleaf'")


class LeafNode(HuffNode):
    '''叶节点'''

    def __init__(self, value=0, freq=0):
        super(LeafNode, self).__init__()
        self.value = value
        self.weight = freq

    def isleaf(self):
        return True

    def get_weight(self):
        return self.weight

    def get_value(self):
        return self.value


class IntlNode(HuffNode):
    '''中间节点'''

    def __init__(self, left_child=None, right_chid=None):
        super(IntlNode, self).__init__()
        # 概率相加
        self.weight = left_child.weight + right_chid.weight
        self.left_child = left_child
        self.right_child = right_chid

    def isleaf(self):
        return False

    def get_weight(self):
        return self.weight

    def get_left(self):
        return self.left_child

    def get_right(self):
        return self.right_child


class HuffTree():
    def __init__(self, flag, value=0, freq=0, left_tree=None, right_tree=None):
        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = IntlNode(left_tree.root, right_tree.root)

    def get_weight(self):
        return self.root.get_weight()

    def traverse_huffman_tree(self, root, code, char_freq):
        '''递归遍历哈夫曼树，得到最优码，将最有码保存在字典char_freq中。'''
        if root.isleaf():
            char_freq[root.get_value()] = code
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code + '0', char_freq)
            self.traverse_huffman_tree(root.get_right(), code + '1', char_freq)


def buildHuffmanTree(list_hufftrees):
    '''构造哈夫曼树'''
    while len(list_hufftrees) > 1:
        list_hufftrees.sort(key=lambda x: x.get_weight())  # 按权重排序
        temp1 = list_hufftrees[0]
        temp2 = list_hufftrees[1]
        list_hufftrees = list_hufftrees[2:]

        # 构建新的哈夫曼节点
        new_hufftree = HuffTree(1, 0, 0, temp1, temp2)
        list_hufftrees.append(new_hufftree)

    return list_hufftrees[0]  # 最后剩余的那颗树即构造完成的那棵树


def compress(input_f, out_put_f):
    '''压缩文件参数，前者为输入文件的地址和名字，后者为输出文件的地址和名字'''
    f = open(input_f, 'rb')  # 二进制方式打开文件
    filedata = f.read()
    filesize = f.tell()  # 文件的字节总数

    # 字符字典
    char_freq = {}
    for x in range(filesize):
        tem = filedata[x]
        if tem in char_freq.keys():
            char_freq[tem] += 1
        else:
            char_freq[tem] = 1

    # 构造哈夫曼树
    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    # 统计各个值的频率信息保存叶子节点的个数
    length = len(char_freq.keys())
    output = open(out_put_f, "wb")

    # int四个字节，将其分成四个字节写入输出文件
    a4 = length & 255
    length = length >> 8
    a3 = length & 255
    length = length >> 8
    a2 = length & 255
    length = length >> 8
    a1 = length & 255
    output.write(six.int2byte(a1))
    output.write(six.int2byte(a2))
    output.write(six.int2byte(a3))
    output.write(six.int2byte(a4))  # 八比特二进制数据，以二进制读入时数据的模样

    # 将每个值出现的频率压缩入文件方便解压
    for x in char_freq.keys():
        output.write(six.int2byte(x))
        temp = char_freq[x]
        a4 = temp & 255
        temp = temp >> 8
        a3 = temp & 255
        temp = temp >> 8
        a2 = temp & 255
        temp = temp >> 8
        a1 = temp & 255
        output.write(six.int2byte(a1))
        output.write(six.int2byte(a2))
        output.write(six.int2byte(a3))
        output.write(six.int2byte(a4))

    # 构造哈夫曼树
    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.root, "", char_freq)

    # 压缩
    code = ''
    for i in range(filesize):
        key = filedata[i]
        code = code + char_freq[key]
        out = 0
        while len(code) > 8:
            for x in range(8):
                out = out << 1
                if code[x] == '1':
                    out = out | 1
            code = code[8:]
            output.write(six.int2byte(out))
            out = 0

        # 处理剩下来的不满8位的code
    output.write(six.int2byte(len(code)))
    out = 0
    for i in range(len(code)):
        out = out << 1
        if code[i] == '1':
            out = out | 1
    for i in range(8 - len(code)):
        out = out << 1
    # 把最后一位给写入到文件当中
    output.write(six.int2byte(out))

    # 6. 关闭输出文件，文件压缩完毕
    f.close()
    output.close()


def decompress(input_f, output_f):
    '''解压文件，前者为要解压的文件地址和名字，后者为存放解压文件的地址和名字'''
    f = open(input_f, 'rb')
    filedata = f.read()
    filesize = f.tell()

    # 读取叶节点的个数即压缩入的length
    a1 = filedata[0]
    a2 = filedata[1]
    a3 = filedata[2]
    a4 = filedata[3]
    j = 0
    j = j | a1
    j = j << 8
    j = j | a2
    j = j << 8
    j = j | a3
    j = j << 8
    j = j | a4
    length = j

    # 将各个编码的频率以及本身信息读取出来。
    char_freq = {}
    for i in range(length):
        c = filedata[4 + i * 5 + 0]  # 读取的为字符
        a1 = filedata[4 + i * 5 + 1]
        a2 = filedata[4 + i * 5 + 2]
        a3 = filedata[4 + i * 5 + 3]
        a4 = filedata[4 + i * 5 + 4]
        j = 0
        j = j | a1
        j = j << 8
        j = j | a2
        j = j << 8
        j = j | a3
        j = j << 8
        j = j | a4
        char_freq[c] = j

    # 重建哈夫曼树
    list_hufftrees = []
    for x in char_freq.keys():
        tem = HuffTree(0, x, char_freq[x], None, None)
        list_hufftrees.append(tem)

    tem = buildHuffmanTree(list_hufftrees)
    tem.traverse_huffman_tree(tem.root, '', char_freq)

    # 进行解压缩
    output = open(output_f, 'wb')
    code = ""
    currnode = tem.root
    for x in range(length * 5 + 4, filesize):
        c = filedata[x]
        for i in range(8):  # 检测每一位是什么
            if c & 128:
                code += '1'
            else:
                code += '0'
            c = c << 1

        while len(code) > 24:  # 最后剩余的不到八位的code加上长度总共占用了16比特，然而还可能与之前的code有联系，所以取24为单位
            if currnode.isleaf():
                tem_byte = six.int2byte(currnode.get_value())
                output.write(tem_byte)
                currnode = tem.root
            if code[0] == '1':
                currnode = currnode.get_right()
            else:
                currnode = currnode.get_left()
            code = code[1:]

        # 处理最后24位
    sub_code = code[-16:-8]  # 长度编码
    last_length = 0
    for i in range(8):
        last_length = last_length << 1
        if sub_code[i] == '1':
            last_length = last_length | 1

    code = code[:-16] + code[-8:-8 + last_length]
    while len(code) > 0:
        if currnode.isleaf():
            tem_byte = six.int2byte(currnode.get_value())
            output.write(tem_byte)
            currnode = tem.root
        if code[0] == '1':
            currnode = currnode.get_right()
        else:
            currnode = currnode.get_left()
        code = code[1:]
    if currnode.isleaf():
        tem_byte = six.int2byte(currnode.get_value())
        output.write(tem_byte)
        currnode = tem.root

    f.close()
    output.close()


if __name__ == '__main__':
    i = 'text.txt'
    j = 'output1.txt'
    compress(i, j)
    k='output2.txt'
    decompress(j,k)
