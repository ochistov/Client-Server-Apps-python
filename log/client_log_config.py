import logging
import os.path

logger = logging.getLogger('client')

formatter = logging.Formatter("%(asctime)s - %(levelname)-8s - %(module)-8s - %(message)s ")

storage_name = 'log-storage'
if not os.path.exists(storage_name):
    os.mkdir(storage_name)
filename = os.path.join(storage_name, 'client.log')

fh = logging.FileHandler(filename, encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Logging test run')