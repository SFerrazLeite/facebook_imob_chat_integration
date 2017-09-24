from aiohttp import web

from facebook_imob_chat_integration.app import app


def main():
    web.run_app(app, port=6548)

if __name__ == '__main__':
    main()
