from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from imob_async_service.app import init_app


class TestConfig(AioHTTPTestCase):
    async def get_application(self):
        return init_app(config={
            'IMOB_CUSTOM_SETTING': 'foobar'
        })

    @unittest_run_loop
    async def test_status(self):
        self.assertEqual(
            (await self.get_application())['config']['IMOB_CUSTOM_SETTING'],
            'foobar'
        )
