import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timezone
from services import research_news as news
from services.research_ai import ResearchError

class NewsTests(unittest.TestCase):
    def setUp(self):
        news._cache.clear()
        self.week = datetime.now(timezone.utc).date().isoformat()
    def test_filters_cache_and_safe_links(self):
        response = Mock()
        response.json.return_value = {'articles': [{'title':'Contexto', 'url':'https://example.org/news'}, {'url':'javascript:alert(1)'}, {'url':'https://example.org/news'}]}
        with patch.object(news.requests, 'get', return_value=response) as get:
            result = news.search('uva', self.week, 'trade')
            self.assertEqual(len(result['articles']), 1)
            self.assertIn('Peru', result['query'])
            self.assertIn('grape', get.call_args.kwargs['params']['query'])
            self.assertTrue(news.search('uva', self.week, 'trade')['cached'])
            self.assertEqual(get.call_count, 1)
    def test_provider_failure_is_explicit(self):
        with patch.object(news.requests, 'get', side_effect=news.requests.Timeout):
            with self.assertRaises(ResearchError) as error: news.search('palta', self.week, 'weather')
            self.assertEqual(error.exception.code, 'news_unavailable')
    def test_no_articles_is_valid(self):
        response = Mock(); response.json.return_value = {'articles': []}
        with patch.object(news.requests, 'get', return_value=response):
            self.assertEqual(news.search('palta', self.week, 'trade')['articles'], [])
    def test_unknown_product_and_old_dates_rejected(self):
        for args in [('other',self.week,'trade'), ('palta','2020-01-01','trade')]:
            with self.assertRaises(ResearchError): news.search(*args)
    def test_invalid_json_shape_not_empty_success(self):
        response = Mock(); response.json.return_value = {'error':'failure'}
        with patch.object(news.requests, 'get', return_value=response):
            with self.assertRaises(ResearchError): news.search('uva',self.week,'trade')

if __name__ == '__main__': unittest.main()
