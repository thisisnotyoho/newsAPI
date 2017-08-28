#!/usr/bin/env python3
from news import News
import textwrap


def print_article(article, linewidth=80):
    print('='*40)
    print(textwrap.fill(article['title'],width=linewidth))
    print(textwrap.fill(article['description'],width=linewidth))
    print('\nurl: ' + article['url'] )
    print('Published: ' + article['publishedAt'])
    print('='*80)    
        
if __name__ == "__main__":
    _SHOW_COUNT = 6
    n = News()
    sources = [x for x in n.sources if x['language'] == 'en']
    sources = [x for x in   sources if x['category'] == 'business']
    for source in sources:
        if(source['language'] != 'en'): continue
        if 'latest' in source['sortBysAvailable']:
            articles = n.get_articles(source['id'],sortBy='latest')
        else:
            articles = n.get_articles(source['id'])
        print(source['name'])
        
        end = min(_SHOW_COUNT,len(articles))
        for i in range(0,end):
            print_article(articles[i])

        
            
