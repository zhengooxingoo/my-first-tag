# coding:utf-8
from collections import defaultdict
import os
import jieba
import jieba.analyse
import sys
reload (sys)
sys.setdefaultencoding( "utf-8" )


class Keywords(object):
    name = os.path.abspath(".")+"/tags/temp/wordfrequency.txt"
    #name = "/home/zxingoo/supertags/tags/temp/wordfrequency.txt"
    def __init__(self, txt):
        print self.name
        self.txt = txt

    # 使用 add_word(word, freq=None, tag=None) 和 del_word(word) 可在程序中动态修改词典。
    # 使用 suggest_freq(segment, tune=True) 可调节单个词语的词频，使其能（或不能）被分出来。
    # 主要步骤：分词——过滤停用词（略）——替代同义词——计算词语在文本中出现的概率  
    
    def tf_idf(self):
        
        jieba.load_userdict(os.path.abspath(".") + "/tags/material/userdict.txt")
        #jieba.load_userdict("/home/zxingoo/supertags/tags/material/userdict.txt")
        #jieba.suggest_freq("达康书记", tune = True)
        #jieba.suggest_freq("人民的名义", tune = True)       
        
        seg_list = jieba.cut(self.txt, cut_all=False)

   
        stopwords_filename = os.path.abspath(".")+"/tags/material/stopwords.txt"  # stopwords
        #stopwords_filename = "/home/zxingoo/supertags/tags/material/stopwords.txt"
        stopwords = {}
        f = open(stopwords_filename, 'r')
        line = f.readline().rstrip()
        lines_total= 0
        while line:
            stopwords.setdefault(line, 0)
            stopwords[line.decode('utf-8')] = 1
            line = f.readline().rstrip()
            lines_total +=1
        f.close()
        print lines_total
        seg_list = [i for i in seg_list if i not in stopwords]
        tmp_list = "/".join(seg_list).encode("utf-8")

        combinewords_filename = os.path.abspath(".")+"/tags/material/combinewords.txt"  # combine_dict
        #combinewords_filename = "/home/zxingoo/supertags/tags/material/combinewords.txt"
        combine_dict = {}
        for line in open(combinewords_filename, "r"):
            seperate_word = line.strip().split("\t")
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[seperate_word[i]] = seperate_word[0]
                
        for key,value in combine_dict.items():
	        print key,value
	        
        seg_list_2 = ""
        for word in tmp_list.split("/"):
			if word in combine_dict:
				word = combine_dict[word]
				seg_list_2 += word
			else:
				seg_list_2 += word


                
        seg_list_3 = jieba.cut(seg_list_2, cut_all = False)  
        seg_list = jieba.cut(seg_list_2, cut_all = False)     
        # 关键词提取所使用逆向文件频率（IDF）文本语料库可以切换成自定义语料库的路径。    
        tf = jieba.analyse.extract_tags(self.txt, topK=500, withWeight=False)
        seg_list_3 = [i for i in seg_list_3 if i in tf]
        
        wordfreq = defaultdict(int)
        for i in seg_list_3:
            wordfreq[i] += 1
        print len(wordfreq)
        #wordfreq = [(i, wordfreq[i]) for i in wordfreq]       
        #wordfreq.sort(key=lambda x: x[1], reverse=True)
        #with open(self.name,'w') as p:
        #    p.write(u"、 ".join ([ i[0] + u'（' + str(i[1]) +u'）' for i in wordfreq]))
        return wordfreq
        #w=r' '.join(seg_list_3)
        #return w

if __name__ == "__main__":
    #file_path ="/home/zxingoo/supertags/tags/temp/tmp.txt"
    with open(file_path, 'r')as f:
        lines=f.readlines()
    txt = u''.join(lines)
    word= Keywords(txt).tf_idf()


