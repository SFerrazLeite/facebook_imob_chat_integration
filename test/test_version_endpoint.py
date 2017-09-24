from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from facebook_imob_chat_integration import __version__, __project__, __revision__
from facebook_imob_chat_integration.app import init_app


class TestVersion(AioHTTPTestCase):
    async def get_application(self):
        return init_app()

    @unittest_run_loop
    async def test_get_version(self):
        response = await self.client.get('/version')
        self.assertEqual(response.status, 200)

        json = await response.json()
        self.assertEqual(json['version'], __version__)
        self.assertEqual(json['project'], __project__)
        self.assertEqual(json['revision'], __revision__)
