import sys
import gc


def main():
    if not sys.version_info >= (3, 5):
        print('[Startup] Version of python is not at least version 3.5')
        sys.exit(1)

    import asyncio
    from bot.bot import LambdaBot

    loops = 0
    max_wait = 60

    try:
        lb = LambdaBot()
        print('[Startup] Starting up...')
        lb.run()
    except Exception as e:
        print('[Startup] An error occurred:', e)

    gc.collect()

if __name__ == '__main__':
    main()




