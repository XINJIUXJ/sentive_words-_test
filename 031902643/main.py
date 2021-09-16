import copy
import re
from zhconv import convert

org_path = input()  # 输入文本路径
words_path = input()  # 输入敏感词路径
ans_path = input()  # 输入答案路径

org_txt = []  # 进行操作的串
op_txt = []  # 原文串
words_txt = []
ans_txt = []

ans = []
num = 0

def read_file():
    global words_txt, org_txt
    with open(org_path, 'r+', encoding='utf-8') as f:
        org_txt = f.readlines()  # org_txt代表整个org文本
        f.close()

    with open(words_path, 'r+', encoding='utf-8') as f:
        words_txt = f.readlines()  # words_txt代表整个words文本
        f.close()


class Node(object):
    def __init__(self):
        self.next = {}  # 相当于指针，指向树节点的下一层节点
        self.fail = None  # 失配指针，这个是AC自动机的关键
        self.isWord = False  # 标记，用来判断是否是一个标签的结尾
        self.word = ""  # 用来储存标签


class AcAutomation(object):
    def __init__(self, user_dict_path):
        self.root = Node()
        self.user_dict_path = user_dict_path

    def add(self, word):
        temp_root = self.root
        for char in word:
            if char not in temp_root.next:
                temp_root.next[char] = Node()
            temp_root = temp_root.next[char]

        temp_root.isWord = True
        temp_root.word = word

    # 添加文件中的关键词
    def add_keyword(self):
        with open(self.user_dict_path, "r", encoding="utf-8") as file:
            for line in file:
                self.add(line.strip())

    def make_fail(self):
        temp_que = [self.root]
        while len(temp_que) != 0:
            temp = temp_que.pop(0)
            for key, value in temp.next.item():
                if temp == self.root:
                    temp.next[key].fail = self.root
                else:
                    p = temp.fail
                    while p is not None:
                        if key in p.next:
                            temp.next[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        temp.next[key].fail = self.root
                temp_que.append(temp.next[key])

    def search(self, content):
        global num, ans
        num += 1
        p = self.root
        result = set()
        index = 0
        while index < len(content) - 1:
            current_position = index
            while current_position < len(content):
                word = content[current_position]

                while word in p.next is False and p != self.root:
                    p = p.fail
                if word in p.next:
                    p = p.next[word]
                else:
                    p = self.root

                if p.isWord:
                    end_index = current_position + 1
                    result.add((p.word, end_index - len(p.word), end_index))
                    break

                current_position += 1
            p = self.root
            index += 1
        if result != set():
            for i in result:
                ans.append('Line'+str(num)+': <'+i[0]+'> '+i[0]+'\n')
            return result
        return 0


def deal():
    tot = 0
    txt = copy.deepcopy(org_txt)
    # 将原文本中的特殊字符删去：
    for i in txt:
        i = i.replace('\n', '').replace('\r', '')  # 去掉换行符
        i = re.sub(u'([^\u3400-\u4db5\u4e00-\u9fa5a-zA-Z])', '*', i)
        i = convert(i, 'zh-hans')  # 繁体转简体
        i = i.lower()  # 大写换小写
        op_txt.append(i)

    for i in op_txt:
        query = list(i)
        res = ac.search(query)
        if res != 0:
            tot += 1
    f = open(ans_path, mode='w', encoding='utf-8')
    f.writelines('Total: '+str(tot)+'\n')
    for i in ans:
        f.writelines(str(i))
    f.close()


if __name__ == "__main__":
    read_file()
    ac = AcAutomation(user_dict_path=words_path)
    ac.add_keyword()  # 添加关键词到AC自动机
    deal()
