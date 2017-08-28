import urllib.request
import json
import os


class News():
    """ The news class represents the interface to the news API at http://newsapi.org.
    On initialization, the source list is fetched from the newsapi.

    The NewsAPI requires an API key.  See https://newsapi.org/register
    to get an API Key.  This key must be passed in the constructor, through
    the newsconfig module's api_key variable, or through the NEWS_API_KEY
    environment variable.
    """

    @property
    def categories(self):
        return {x['category'] for x in self.sources}
        
    @property
    def sources(self):
        """ Full list of sources retrieved when the class was initialized.
        see News.get_sources for more information."""
        return self._sources

    class NewsApiError(Exception):
        pass
    
    def __init__(self,api_key=None):
        if api_key == None:
            self.api_key = self._get_api_key_from_external()
        else:
            self.api_key = api_key

        self._api_header = {'X-Api-Key' : self.api_key}

        self._update_sources()

    def get_sources(self, **kwargs):
        """Gets sources from the NewsAPI endpoint. Since News.sources should be
        a superset of these, filtering those should be preferred.

        param kwargs - These are optional parameters passed to the newsapi 
                       source endpoint.
            Currently the only parameters supported are:

                category - Filter by source category.
                    Examples: 'business','entertainment'

                language - ISO-639-1 code of the language you want sources
                    for. Examples: 'en','de','fr'

                country  - The 2-letter ISO 3166-1 code of the country you would like
                    to get sources for.
                    Examples: 'us', 'au', 'de', 'gb'
            
            More may be added in the future.

        returns - List of dicts of source information.
        """
        
        url = 'https://newsapi.org/v1/sources?'
        for x in kwargs.items():
            url+=x[0]+'='+x[1]
        req = urllib.request.Request( url, headers=self._api_header)
        with urllib.request.urlopen(req) as fd:
            sources = json.loads(fd.read().decode())
        if sources['status'] != 'ok':
            raise self.NewsApiError(sources['code'],sources['message'])
        sources = [x for x in sources['sources'] if x['id'] not in blacklist]
        return sources
        
    def get_articles(self, source, sortBy=None):
        """ Gets articles from the newsapi endpoint. """
        url = 'https://newsapi.org/v1/articles?'
        url += 'source=' + source
        if sortBy is not None:
            url += '&sortBy=' + sortBy
        req = urllib.request.Request(url,headers=self._api_header)
        with urllib.request.urlopen(req) as fd:
            articles = json.loads(fd.read().decode())
        if articles['status'] != 'ok':
            raise self.NewsApiError(sources['code'],sources['message'])
        articles = articles['articles']
        return articles

    def _get_api_key_from_external(self):
        """ Internal method to search for a config module or environment variable
        for the NewsAPI key. """
        try:
            import newsconfig
            return newsconfig.api_key
        except:
            pass
        tmp = os.getenv('NEWS_API_KEY')
        if tmp is None:
            raise self.NewsApiError(
            """The NewsAPI requires an API key.  See https://newsapi.org/register
            to get an API Key.  This key must be passed in the constructor, through
            the newsconfig module's api_key variable, or through the NEWS_API_KEY
            environment variable.
            """
            )
    
    def _update_sources(self):
        url = 'https://newsapi.org/v1/sources'
        req = urllib.request.Request( url, headers=self._api_header)
        with urllib.request.urlopen(req) as fd:
            sources = json.loads(fd.read().decode())
        if sources['status'] != 'ok':
            raise self.NewsApiError(sources['code'],sources['message'])
        self._sources = sources['sources']






















