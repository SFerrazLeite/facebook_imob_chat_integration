import asyncio

import logging.config
from logging import Logger

from imob_async_service.app import app


class ImobLogger(Logger):
    @staticmethod
    def info(msg, *args, **kwargs):
        print(msg, args, kwargs)


def main():
    loop = asyncio.get_event_loop()
    app_handler = app.make_handler(access_log_format='%Tf')
    f = loop.create_server(app_handler, '127.0.0.1', '6534')
    srv = loop.run_until_complete(f)
    print('standalone server is serving on http://{}:{}'.format(*srv.sockets[0].getsockname()))

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(message)s %(request_time_frac)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'aiohttp.access': {
                'level': 'INFO',
                'handlers': ['default']
            }
        }
    })

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app_handler.finish_connection(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()


if __name__ == '__main__':
    main()
