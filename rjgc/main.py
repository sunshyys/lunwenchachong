# coding:gbk
import os
import re
import cProfile
import gensim
import jieba

jieba.setLogLevel(jieba.logging.INFO)


# ��ȡָ��·�����ļ�����
def get_file_contents(path):
    str  = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


# ����ȡ�����ļ������Ƚ���jieba�ִʣ�Ȼ���ٰѱ����š�ת����ŵ�������Ź��˵�
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    result = jieba.lcut(string)
    return result


# ���Ե��ı����﷨�������Ҫ�أ�����������������ɸ��ʻ�ļ���
def convert_corpus(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus


# �������֮������ݣ�ͨ������gensim.similarities.Similarity�����������ƶ�
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


if __name__ == '__main__':
    print("������ԭ����·����")
    path1 = input()
    print("������Ҫ���ص�����·����")
    path2 = input()
    if not os.path.exists(path1) :
        print("����ԭ���ļ������ڣ�")
        exit()
    if not os.path.exists(path2):
        print("��Ϯ�������ļ������ڣ�")
        exit()
    save_path = "C:\\Users\Administrator\PycharmProjects\\rjgc\save.txt"    #����������·��
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    print("�������ƶȣ� %.2f"%similarity)
    cProfile.run("get_file_contents(path1)")
    cProfile.run("get_file_contents(path2)")
    cProfile.run("filter(str1)")
    cProfile.run("filter(str2)")
    cProfile.run("convert_corpus(text1,text2)")
    cProfile.run("calc_similarity(text1,text2)")
    #�����ƶȽ��д��ָ���ļ�
    f = open(save_path, 'w', encoding="utf-8")
    f.write("python"+" "+"main.py"+" "+path1+" "+path2+" "+"�������ƶȣ� %.2f"%similarity)
    f.close()
