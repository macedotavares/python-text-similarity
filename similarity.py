#!/usr/bin/env python
#-*- coding: utf-8 -*-

import operator, collections, os, sys, re, string, nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

rootdir = "."
target = sys.argv[1]

similarity_threshold = 0.1

stop_words = set(stopwords.words('english')).union(set(stopwords.words('portuguese')))
md_regex = re.compile(r'.*md$')
tag_regex = re.compile(r'#([-_\d\w]+)')
link_regex = re.compile(r'\[\[(.*?)[|#]')


def read(file):
    with open(file, 'r') as f:
        content = f.read()
        f.close()
    return content.lower()

def remove_numbers(input_str):
    result = re.sub(r'\d+', '', input_str)
    return result

def remove_whitespace(input_str):
    result = re.sub(r'[\t\n\r]', '', input_str)
    return result    

def remove_punctuation(input_str):
    result = input_str.translate(str.maketrans('', '', string.punctuation))
    return result

def remove_stopwords(input_str):
    tokens = word_tokenize(input_str)
    result = [i for i in tokens if not i in stop_words]
    return result

def preprocess(file):
    return remove_stopwords(remove_whitespace(remove_punctuation(remove_numbers(read(file)))))

def extract_keywords(input_str):
	tags = set(re.findall(tag_regex, input_str))
	links = set(re.findall(link_regex, input_str))
	return tags.union(links)

def jaccard_similarity(list1, list2): 
	intersection = set(list1).intersection(set(list2))
	union = set(list1).union(set(list2))
	if len(union)>0:
		return float(len(intersection) / len(union))
	else: return 0.0
		
raw_target = read(sys.argv[1])
preprocessed_target = preprocess(sys.argv[1])

for root, dirs, files in os.walk(rootdir):
	for other_file in files:
		if md_regex.match(other_file):
			other_file = os.path.join(root, other_file)
			preprocessed_other = preprocess(other_file)
			raw_other = read(other_file)

			text_similarity = jaccard_similarity(preprocessed_target, preprocessed_other)
			#print(text_similarity)
			keyword_similarity = jaccard_similarity(extract_keywords(raw_target), extract_keywords(raw_other))
			#print(keyword_similarity)
			similarity = (0.25*text_similarity) + (0.75*keyword_similarity)
			#print(similarity)
			if similarity > similarity_threshold:
				print(other_file + '\t\t\t\t\t' + str(round(similarity,3)*100)+'%')