import sys
import unittest

sys.path.insert(0, '../')
import twitterDataRankings
import config

class TestRanking(unittest.TestCase):
    def test_rank_word(self):
        
        rank = twitterDataRankings.Ranking()
        top_words, top_f = rank.rank_list(config.search_word)

        #test if it's top 10
        assert len(top_words) == 10
        assert len(top_f) == 10
        #test word data type
        for word in top_words:
            assert type(word) == type('')
        
        #test frequency data type
        for f in top_f:
            assert type(f) == type(0)

        #test invalid keyword
        #invalid type
        top_words = rank.rank_list([])
        assert 'Invalid Keyword'
        #valid type but blank string
        top_words = rank.rank_list('')
        assert 'Invalid Keyword'

if __name__ == '__main__':
    unittest.main()

        