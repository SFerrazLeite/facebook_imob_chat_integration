from os import environ, path

from aiohttp import web

from imob_async_service.endpoints import ROUTES


def init_app(config=None):
    async_app = web.Application()
    async_app['config'] = config or {}

    for method, route, handler in ROUTES:
        async_app.router.add_route(method, route, handler)

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
