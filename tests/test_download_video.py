

import pytest
from faker import Faker
import arrow
from tenacity import retry, stop_after_attempt
import random



class TestBaiduSpider(object):
    def test_add(self):
        assert 1 + 1 == 2

    def test_false(self):
        fak = Faker('zh_CN')
        print('name: ', fak.name())
        print('address: ', fak.address())
        print('text: ', fak.text())
        assert True

    def test_parse_time(self):
        time_str = '2020-1-4'
        cc = arrow.get(time_str)
        print(cc)
        local = arrow.utcnow()

        print(local.format())
        print(local.humanize(locale='zh_CN'))
        assert True

    @retry(stop=stop_after_attempt(7))
    def do_something(self):
        print("I'm retrying!!!")
        raise Exception

    def test_retry(self):
        print(self.get_info())
        print(123)
        print(123)
        assert True

    @retry
    def get_info(self):
        if random.randint(0, 10) > 1:
            print('random number error')
            raise IOError("Error occurred!!")
        else:
            return "HOHO"

    def test_assert(self):
        assert True