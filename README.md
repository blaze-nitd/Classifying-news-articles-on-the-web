## Classifying-news-articles-on-the-web
Confused whether an article on the web is related to tech or not? Well this project has the code in it which can easily classify whether an article on the web is a tech article or a non-tech article.
There are two files in this project. Both does the same thing. The first one solves the given problem with the help of K Nearest Neighbour Algorithm and the second one solves the problem with the help
of Naive Bayes Classifier.
Web scraping is done with BeautifulSoup library of python. nltk(Natural Language Toolkit) library of Python is used to tokenize the text and carry some useful operations.

## Getting started

**I)** Use Python3 for running the codes on the project.  
This code will require some libraries which you need to install:
Following are the libraries' names with the required steps:
1. *requests*  
run the command: 

```shell
pip install requests

```  

2. *bs4*  
run the command : 

```shell
sudo apt-get install python3-bs4

```  

3. *nltk*  
run the command : 

```shell
sudo apt-get install python-numpy python-nltk

```  


**II)** *Also you have to install the stopwords data from nltk data.  
Run the following two lines in python interpreter:*  

```python
import nltk 
nltk.download("stopwords")
``` 
**III)** *Replace "http://doxydonkey.blogspot.in/" with the article's URL in double quote.
Then open the URL's page source and locate where the actual text is contained in the article. Replace "post-body" with that name.*

**IV)** *In the command line  run:*  

```shell
python ClassifierWithKNN.py "http://doxydonkey.blogspot.in/" "post-body"
```  
---
Note: file-name here refers to either of the two files included in this repository
