import aiohttp, time
from aiohttp import ClientConnectorError, ClientError
from twisted.plugins.twisted_reactors import asyncio
from db import RedisClient

VAILD_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def testSingleProxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')

                    real = 'http://' + proxy
                    print('Testing')

                    async with session.get(TEST_URL, proxy = real, timeout = 10) as resp:
                        if resp.status in VAILD_STATUS_CODE:
                            self.redis.max(proxy)
                        else:
                            self.redis.decrease(proxy)
            except(ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)

    def run(self):
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()

            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                testProxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.testSingleProxy(proxy) for proxy in testProxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print(e.args)