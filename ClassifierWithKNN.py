
# coding: utf-8

# In[53]:


import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
import urllib.request
from heapq import nlargest


# In[54]:


def getWashPostText(url,token):
    try:
        page=urllib.request.urlopen(url).read().decode('utf8')
    except:
        return (None,None)
    soup=BeautifulSoup(page,"lxml")
    if(soup is None):
        return (None,None)
    text=""
    if(soup.find_all(token) is not None):
        text=''.join(map(lambda p: p.text, soup.find_all(token)))
        soup2=BeautifulSoup(text,"lxml")
        if(soup2.find_all('p') is not None):
            text=''.join(map(lambda p: p.text, soup.find_all('p')))
    return text, soup.title.text


# In[55]:


def getNYTText(url,token):
    page=urllib.request.urlopen(url).read().decode('utf8')
    soup=BeautifulSoup(page,"lxml")
    title=soup.find('title').text
    mydivs=soup.find_all("p" , {"class":"story-body-text story-content"})
    text=''.join(map(lambda p:p.text,mydivs))
    return text,title 


# In[56]:


def scrapeSource(url,magicFrag='2015',scraperFunction=getNYTText, token='None'):
    urlBodies={}
    response=urllib.request.urlopen(url).read().decode('utf8')
    soup=BeautifulSoup(response,"lxml")
    numerror=0
    for a in soup.find_all('a'):
        try:
            url=a['href']
            if((url not in urlBodies) and ((magicFrag is not None and magicFrag in url) or magicFrag is None)):
                body=scraperFunction(url,token)
                if(body and len(body)>0):
                    urlBodies[url]=body
                print(url)
        except:
            numerror=numerror+1
    return urlBodies
                


# In[65]:


class FrequencySummarizer:
    def __init__(self, min_cut=0.1,max_cut=0.9):
        self._max_cut=max_cut
        self._min_cut=min_cut
        self._stopwords=set(stopwords.words('english')+list(punctuation)+[u"'s",'"'])
    def _compute_frequencies(self, word_sent, customStopWords=None):
        freq=defaultdict(int)
        if customStopWords is None:
            stopwords=set(self._stopwords)
        else:
            stopwords=set(customStopWords).union(self._stopwords)
        for sentence in word_sent:
            for word in sentence:
                if(word not in stopwords):
                    freq[word]+=1
        m=float(max(freq.values()))
        for word in list(freq.keys()):
            freq[word]=freq[word]/m
            if(freq[word]>=self._max_cut or freq[word]<=self._min_cut):
                del freq[word]
        return freq
    def extractFeatures(self, article, n, customStopWords=None):
            text=article[0]
            title=article[1]
            sentences=sent_tokenize(text)
            word_sent=[word_tokenize(sent.lower()) for sent in sentences]
            self._freq=self._compute_frequencies(word_sent, customStopWords)
            if n<0:
                return nlargest(len(self._freq.keys()),self.freq,key=self._freq.get)
            else:
                return nlargest(n,self._freq,key=self._freq.get)
            
    
    def extractRawFrequencies(self,article):
        text=article[0]
        title=article[1]
        sentences=sent_tokenize(text)
        word_sent=[word_tokenize(sents.lower()) for sents in sentences]
        freq=dafaultdict(int)
        for s in word_sents:
            for word in s:
                if word not in self._stopwords:
                    freq[word]+=1
        return freq
    
    def summarize(self,article,n):
        text=article[0]
        title=article[1]
        sentences=sent_tokenize(text)
        word_sent=[word_tokenize(s.lower()) for s in sentences]
        self._freq=self._compute_frequencies(word_sent)
        ranking=dafaultdict(int)
        for i,sentence in enumerate(word_sent):
            for word in sentence:
                if word in self._freq:
                    ranking[i]+=self._freq[word]
        sentences_index=nlargest(n,ranking, key=ranking.get)
        return [sentences[j] for j in sentences_index]
    
        


# In[64]:


urlWashingtonPostNonTech="https://www.washingtonpost.com/sports"
urlNewYorkTimesNonTech="https://www.nytimes.com/section/sports"
urlWashingtonPostTech="https://www.washingtonpost.com/business/technology"
urlNewYorkTimesTech="https://www.nytimes.com/section/technology"

washingtonPostTechArticles=scrapeSource(urlWashingtonPostTech,'2017',getWashPostText,'article')
washingtonPostNonTechArticles=scrapeSource(urlWashingtonPostNonTech,'2017',getWashPostText,'article')
newYorkTimesTechArticles=scrapeSource(urlNewYorkTimesTech,'2017',getNYTText,None)
newYorkTimesNonTechArticles=scrapeSource(urlNewYorkTimesNonTech,'2017',getNYTText,None)


# In[68]:


articleSummaries = {}
for techUrlDictionary in [newYorkTimesTechArticles,washingtonPostTechArticles]:
    for articleUrl in techUrlDictionary:
        if(len(techUrlDictionary[articleUrl][0])>0):
            fs=FrequencySummarizer()
            summary=fs.extractFeatures(techUrlDictionary[articleUrl],25)
            articleSummaries[articleUrl]={'feature-vector':summary,'label':'Tech'}

for techUrlDictionary in [newYorkTimesNonTechArticles,washingtonPostNonTechArticles]:
    for articleUrl in techUrlDictionary:
        if(len(techUrlDictionary[articleUrl][0])>0):
            fs=FrequencySummarizer()
            summary=fs.extractFeatures(techUrlDictionary[articleUrl],25)
            articleSummaries[articleUrl]={'feature-vector':summary,'label':'Non-Tech'}


    


# In[69]:


def getDoxyDonkeyText(testUrl,token):
    response = requests.get(testUrl)
    soup = BeautifulSoup(response.content,"lxml")
    page = str(soup)
    title = soup.find("title").text
    mydivs = soup.findAll("div", {"class":token})
    text = ''.join(map(lambda p:p.text,mydivs))
    return text,title


# In[70]:


testUrl = sys.argv[1]
testArticle = getDoxyDonkeyText(testUrl,sys.argv[2])

fs = FrequencySummarizer()
testArticleSummary = fs.extractFeatures(testArticle, 25)


# In[72]:


similarities={}
for articleUrl in articleSummaries:
    oneArticleSummary=articleSummaries[articleUrl]['feature-vector']
    similarities[articleUrl]=len(set(testArticleSummary).intersection(set(oneArticleSummary)))
labels=defaultdict(int)
knn=nlargest(5,similarities,key=similarities.get)
for oneNeighbour in knn:
    labels[articleSummaries[oneNeighbour]['label']]+=1
print("-------------------------------------------------------------------------")
print("Voila!The article is a "+nlargest(1,labels,key=labels.get)[0]+" article")

