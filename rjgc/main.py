# coding:gbk
import os
import re
import cProfile
import gensim
import jieba

jieba.setLogLevel(jieba.logging.INFO)


# 获取指定路径的文件内容
def get_file_contents(path):
    str  = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


# 将读取到的文件内容先进行jieba分词，然后再把标点符号、转义符号等特殊符号过滤掉
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    result = jieba.lcut(string)
    return result


# 忽略掉文本的语法和语序等要素，将其仅仅看作是若干个词汇的集合
def convert_corpus(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus


# 传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


if __name__ == '__main__':
    print("请输入原论文路径：")
    path1 = input()
    print("请输入要查重的论文路径：")
    path2 = input()
    if not os.path.exists(path1) :
        print("论文原文文件不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭版论文文件不存在！")
        exit()
    save_path = "C:\\Users\Administrator\PycharmProjects\\rjgc\save.txt"    #输出结果绝对路径
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    print("文章相似度： %.2f"%similarity)
    cProfile.run("get_file_contents(path1)")
    cProfile.run("get_file_contents(path2)")
    cProfile.run("filter(str1)")
    cProfile.run("filter(str2)")
    cProfile.run("convert_corpus(text1,text2)")
    cProfile.run("calc_similarity(text1,text2)")
    #将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("python"+" "+"main.py"+" "+path1+" "+path2+" "+"文章相似度： %.2f"%similarity)
    f.close()
