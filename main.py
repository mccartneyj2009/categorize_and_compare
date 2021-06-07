import sys

try:
    import pg_scrape
    pg_scrape.working_loop()
    print('Done')
    input()
except ModuleNotFoundError:
    print(sys.exc_info()[1])
    input()