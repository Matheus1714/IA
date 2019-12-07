#!/usr/bin/env python
# coding: utf-8

# In[1]:


#libraries used

import pandas
import nltk
import re
from tqdm import tqdm


# In[2]:


#reading dataet

beginning = 0 #where to start using data
end = 300 #where to end using data

phishing_dataset = pandas.read_csv('verified_online.csv', nrows = end/2)

benign_dataset = pandas.read_csv('Benign_list_big_final.csv', nrows = end/2, header=None)

phishing_dataset.url.tolist()


# In[3]:


#checking dataset size

print(phishing_dataset.shape)
print(benign_dataset.shape)


# In[4]:


#parsing the urls

from urllib.parse import urlparse

phishing_urls = phishing_dataset.url.tolist()

benign_urls = benign_dataset.values.tolist()

phishing_urls_labeled = []

benign_urls_labeled = []

for url in phishing_urls:

    url = [url ,1]
    
    phishing_urls_labeled.append(url)
    
for url in benign_urls:
    
    url = [url[0] ,0]
    
    benign_urls_labeled.append(url)
    
phishing_urls_labeled.extend(benign_urls_labeled)

urls = phishing_urls_labeled
parsed_urls = []

for url in tqdm(urls):
    
    url = [urlparse(url[0]),url[1]]
    
    parsed_urls.append(url)

print(parsed_urls)


# In[5]:


#separaing in paths and domains

registered_domains = []
paths = []

for parsed_url in tqdm(parsed_urls):
    
    if parsed_url[1] == 1:
        registered_domains.append([parsed_url[0].netloc,1])
        paths.append([parsed_url[0].path,1])
    else:
        registered_domains.append([parsed_url[0].netloc,0])
        paths.append([parsed_url[0].path,0])

splitted_paths =[]

for path in tqdm(paths):
    
    split_path = path[0].split('/')
    size_split_path = len(split_path) - 1
    
    if path[1] == 1:
    
        splitted_paths.append([split_path[1:size_split_path],1])
    
    if path[1] == 0:

        splitted_paths.append([split_path[1:size_split_path],0])
    
print(splitted_paths)


# In[6]:


##Seperating words in readable

from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("words-by-frequency.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


# In[7]:


#clean domains

# cleaned_registered_domains = []

# for domain in tqdm(registered_domains):
#     domain[0] = re.sub("\d", "", domain[0]) #remove numbers
#     domain[0] = re.sub("[-]", "", domain[0]) #remove -
#     domain[0] = re.sub("\.[^.]*$", "", domain[0]) #remove evreything after last dot, basically the .com, etc
#     domain[0] = domain[0].replace('www.','') #remove www.
#     domain[0] = domain[0].replace('.','') #remove .
#     domain[0] = domain[0].replace('_','') #remove _
#     domain[0] = domain[0].lower() #make all wdomain[0]ords lowercase
#     domain[0] = infer_spaces(domain[0]).split(" ") #seperate in words
#     for word in domain[0]: #remove single letters
#         if len(word) == 1:
#             domain[0].remove(word)
#     cleaned_registered_domains.append(domain)
# cleaned_registered_domains


# In[8]:


#clean paths

cleaned_splitted_paths = []

for splitted_path in tqdm(splitted_paths):
    
    cleaned_splitted_path = []
    
    for path in splitted_path[0]:
        path = re.sub("\d", "", path) #remove numbers
        path = path.replace('-', '') #remove -
        path = path.replace('.','') #remove .
        path = path.replace('_','') #remove _
        path = path.lower() #make all words lowercase
        path = infer_spaces(path).split(" ") #seperate in words
        
        if path != []: #if not empty
            
            temporary_path = path.copy()
            
            for word in path: #remove single letters
                if len(word) == 1:
                    temporary_path.remove(word)
            path = temporary_path
        cleaned_splitted_path.append(path)
        
    cleaned_splitted_paths.append([cleaned_splitted_path,splitted_path[1]])

cleaned_splitted_paths_flatted = []
    
for l in cleaned_splitted_paths:
    flat_list = [item for sublist in l[0] for item in sublist] #flatten list
    flat_list = list(set(flat_list)) #remove duplicates
    cleaned_splitted_paths_flatted.append([flat_list,l[1]])

cleaned_splitted_paths = cleaned_splitted_paths_flatted 
    
cleaned_splitted_paths


# In[ ]:


#Get trends for domains

# import sys
# from pytrends.request import TrendReq
# import time

# pytrends = TrendReq(
#     retries = 5,
# )

# domains_related_queries = []

# size = end - beginning
# # size = 1

# with tqdm(total = size, file=sys.stdout) as pbar:
    
#     iteration = beginning
    
#     while iteration < end:
#         domain = cleaned_registered_domains[iteration][0]
#         print(domain)
#         try:
#             if len(domain) > 4:
#                 domain = domain[0:4]
#             pytrends.build_payload(kw_list=domain)
#             dictionairy_related_query = pytrends.related_queries()
            
#             related_queries = []

#             for word in domain:
#                 related = dictionairy_related_query[word]['top']['query'].to_list()
#                 related_queries.extend(related)
#             domains_related_queries.append([related_queries,cleaned_registered_domains[iteration][1]])
#             iteration = iteration + 1
#             pbar.set_description('processed: %d' % (1 + iteration))
#             pbar.update(1)
#         except:
#             time.sleep(10)
#             print('what')
#             if (domain == ['']) or (domain == []) :
#                 iteration = iteration + 1
#                 domains_related_queries.append([[''],cleaned_registered_domains[iteration-1][0]])
#                 pbar.set_description('processed: %d' % (1 + iteration))
#                 pbar.update(1)

# for domain in tqdm(cleaned_registered_domains[beginning:end], desc = 'related query loop'):
    
#     try:
#         pytrends.build_payload(kw_list=domain[0])
#         dictionairy_related_query = pytrends.related_queries()
        
#         related_queries = []
        
#         for word in domain[0]:
#             related = dictionairy_related_query[word]['top']['query'].to_list()
#             related_queries.extend(related)
#         domains_related_queries.append([related_queries,domain[1]])
    
#     except:
#         pass


# In[11]:


# splitted_domains_related_queries = []

# for domain_related in domains_related_queries:
    
#     words = []
    
#     for word in domain_related[0]:
        
#         splitted_word = word.split()
#         words.extend(splitted_word)
    
#     splitted_domains_related_queries.append([words,domain_related[1]])


# In[12]:


# print(cleaned_splitted_paths)


# In[16]:


#Get trends for paths

#Get trends for paths

import sys
from pytrends.request import TrendReq
import time


pytrends = TrendReq(
    retries = 5,
)

paths_related_queries = []

size = end - beginning

with tqdm(total = size, file=sys.stdout) as pbar:
    
    iteration = beginning
    
    while iteration<end:
        
        paths = cleaned_splitted_paths[iteration][0]
        # print(paths)
        
        if (paths!=[]) and (paths != ['']):
            for path in paths:

                path_related_queries = []
                
                try:

                    pytrends.build_payload(kw_list=[path])

                    dictionairy_related_queries = pytrends.related_queries()

                    related = dictionairy_related_queries[path]['top']['query'].to_list()
                    # print('related')
                    # print(related)
                    path_related_queries.extend(related)

                    

                except:

                    time.sleep(0.5)
                    if path == '':
                        path_related_queries.extend(path)

            paths_related_queries.append([path_related_queries,cleaned_splitted_paths[iteration-1][1]])
            
            iteration = iteration + 1

            pbar.set_description('processed: %d' % (1 + iteration))

            pbar.update(1)
        else:
            paths_related_queries.append([[''],cleaned_splitted_paths[iteration][1]])
            
            iteration = iteration + 1

            pbar.set_description('processed: %d' % (1 + iteration))

            pbar.update(1)
# for paths in tqdm(cleaned_splitted_paths, desc = 'related query loop'):
    
#     try:
#         pytrends.build_payload(kw_list=paths)
#         dictionairy_related_query = pytrends.related_queries()

#         related_queries = []

#         for path in paths:
#             related_queries.append(related_query)
            
#         paths_related_queries.append(related_queries)
    
#     except:
#         time.sleep(0.01) #google trends only allows 10 per minute
        
    
    
        
# paths_related_queries

# from pytrends.request import TrendReq
# import time

# pytrends = TrendReq(
#     retries = 5,
# )

# paths_related_queries = []

# for paths in tqdm(cleaned_splitted_paths[beginning:end], desc = 'related query loop'):
    
#     path_related_queries = []
    
#     for path in paths[0]:
        
#         try:
            
#             pytrends.build_payload(kw_list=[path])
            
#             dictionairy_related_queries = pytrends.related_queries()
            
#             related = dictionairy_related_queries[path]['top']['query'].to_list()
            
#             path_related_queries.extend(related)
            
#         except:
            
#             time.sleep(0.01) #google trends only allows 10 per minute
        
#     paths_related_queries.append([path_related_queries,paths[1]])


# In[ ]:





# In[17]:


paths_related_queries


# In[18]:


splitted_paths_related_queries = []

for path_related in paths_related_queries:
    
    words = []
    
    for word in path_related[0]:
        
        splitted_word = word.split()
        words.extend(splitted_word)
    
    splitted_paths_related_queries.append([words,path_related[1]])
    

splitted_paths_related_queries


# In[28]:


df_paths_related = pandas.DataFrame(splitted_paths_related_queries)

# df_domains_related = pandas.DataFrame(splitted_domains_related_queries)
try:
    df_paths_exist_related = pandas.read_csv('related_paths.csv', header=None).append(df_paths_related, ignore_index=True)

    # df_domains_exist_related = pandas.read_csv('related_domains.csv', header=None).append(df_domains_related, ignore_index=True)
    
except:
    pass


# In[29]:


# df_domains_related


# In[30]:


try:
    df_paths_exist_related.to_csv(r'related_paths.csv',index=False, header=False)
    # df_domains_exist_related.to_csv(r'related_domains.csv',index=False, header=False)
    print("File already existed")
except:
    # df_domains_related.to_csv(r'related_domains.csv',index=False, header=False)
    df_paths_related.to_csv(r'related_paths.csv',index=False, header=False)
    print("Created a new file")


# In[31]:


df_paths = pandas.DataFrame(cleaned_splitted_paths)

# df_domains = pandas.DataFrame(cleaned_registered_domains)

try:
    df_paths_exist = pandas.read_csv('paths.csv', header=None).append(df_paths, ignore_index=True)

    # df_domains_exist = pandas.read_csv('domains.csv', header=None).append(df_domains, ignore_index=True)

except:
    pass


# In[32]:


try:
    df_paths_exist.to_csv(r'paths.csv',index=False, header=False)
    # df_domains_exist.to_csv(r'domains.csv',index=False, header=False)
    print("File already existed")
except:
    df_domains.to_csv(r'domains.csv',index=False, header=False)
    # df_paths.to_csv(r'paths.csv',index=False, header=False)
    print("Created a new file")


# In[ ]:




