# -*- coding: utf-8 -*-
from proxy import PROXIES
from agents import AGENTS

import random
import logging

logger = logging.getLogger(__name__)

class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                logger.error('error in Request is %s', e)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
#        if "depth" in request.meta and int(request.meta['depth']) <= 2:
#            return False
#        i = random.randint(1, 10)
#        return i <= 2

        #As a result of unstable of free httpproxy, I stop using proxy.
        #If there are some stable proies, just uncomment codes above.
        return False


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
        logger.debug('%s is used for %s', agent, request.url)