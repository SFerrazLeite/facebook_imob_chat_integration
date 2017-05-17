from aiohttp import web

from imob_async_service.app import app


def main():
    web.run_app(app, port=6548)

if __name__ == '__main__':
    main()
