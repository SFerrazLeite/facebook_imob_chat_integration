from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from facebook_imob_chat_integration.app import init_app


class TestStatus(AioHTTPTestCase):
    async def get_application(self):
        return init_app()

    @unittest_run_loop
    async def test_get_status(self):
        response = await self.client.get('/status')
        self.assertEqual(response.status, 200)
        self.assertEqual(await response.json(), {
            'status': 'OK'
        })
