from os import environ, path

from aiohttp import web, ClientSession
from aiohttp.abc import AbstractCookieJar

from facebook_imob_chat_integration.endpoints import ROUTES


class NullCookieJar(AbstractCookieJar):
    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0

    def update_cookies(self, cookies, response_url=None):
        pass

    def filter_cookies(self, request_url):
        return []

    def clear(self):
        pass


def init_app(config=None):
    async_app = web.Application()
    async_app['config'] = config or {}

    for method, route, handler in ROUTES:
        async_app.router.add_route(method, route, handler)

    async def init_http_client(_app):
        _app['client'] = ClientSession(cookie_jar=NullCookieJar())

    async def close_http_client(_app):
        if not _app['client'].closed:
            _app['client'].close()

    async_app.on_startup.append(init_http_client)
    async_app.on_cleanup.append(close_http_client)

    return async_app


def load_environment_variables():
    """
    Loads the configuration environment variables
    :return: Dictionary which holds all ENV variables
    """
    if environ.get('IMOB_DEV_MODE', None) == '1':
        env_file = path.join(path.dirname(__file__), '..', 'development.env')
        with open(env_file, 'r') as fh:
            imob_settings = {
                key.upper(): value.strip()
                for key, value in map(lambda x: x.split('=', 1), fh.readlines())
            }
    else:
        # read settings from environment variables
        imob_settings = {
            key.upper(): value.strip()
            for key, value in filter(
                lambda x: x[0].upper().startswith('IMOB_'),
                environ.items()
            )
        }

    return imob_settings


app = init_app(config=load_environment_variables())
