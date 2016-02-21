# -*- coding: utf-8 -*-

import unittest
from isentia_task.misc.bloomfilter import BLOOMDupeFilter


#Unit test about bloomfilter
class BLOOMDupeFilterTest(unittest.TestCase):
    
    def test_filter(self):
        bloomfilter = BLOOMDupeFilter()
        bloomfilter.open()
        
        r1 = Request('http://scrapytest.org/1')
        r2 = Request('http://scrapytest.org/2')
        r3 = Request('http://scrapytest.org/2')

        assert not bloomfilter.request_seen(r1)
        assert bloomfilter.request_seen(r1)

        assert not bloomfilter.request_seen(r2)
        assert bloomfilter.request_seen(r3)

        bloomfilter.close('finished')

    def test_bloomfilter_path(self):
        r1 = Request('http://scrapytest.org/1')
        r2 = Request('http://scrapytest.org/2')

        path = tempfile.mkdtemp()
        try:
            df = BLOOMDupeFilter(path)
            df.open()
            assert not df.request_seen(r1)
            assert df.request_seen(r1)
            df.close('finished')

            df2 = BLOOMDupeFilter(path)
            df2.open()
            assert df2.request_seen(r1)
            assert not df2.request_seen(r2)
            assert df2.request_seen(r2)
            df2.close('finished')
        finally:
            shutil.rmtree(path)

    def test_request_fingerprint(self):
        """Test if customization of request_fingerprint method will change
        output of request_seen.
        """
        r1 = Request('http://scrapytest.org/index.html')
        r2 = Request('http://scrapytest.org/INDEX.html')

        bloomfilter = BLOOMDupeFilter()
        bloomfilter.open()

        assert not bloomfilter.request_seen(r1)
        assert not bloomfilter.request_seen(r2)

        bloomfilter.close('finished')

        class CaseInsensitiveBLOOMFilter(BLOOMDupeFilter):

            def request_fingerprint(self, request):
                fp = hashlib.sha1()
                fp.update(request.url.lower())
                return fp.hexdigest()

        case_insensitive_bloomfilter = CaseInsensitiveBLOOMFilter()
        case_insensitive_bloomfilter.open()

        assert not case_insensitive_bloomfilter.request_seen(r1)
        assert case_insensitive_bloomfilter.request_seen(r2)

        case_insensitive_bloomfilter.close('finished')