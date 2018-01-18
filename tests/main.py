from wrapper_tests.upsert_test import *
import os
import logging
import sys
import argparse
import signal

logging.getLogger().setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s - %(name)s] %(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)


parser = argparse.ArgumentParser(
                      description='Unit testing for fiery snap.')

parser.add_argument('-config', type=str, default=None,
                    help='toml config for keys and such, see key.toml')


if __name__ == '__main__':
    unittest.main()
    os.kill(os.getpid(), signal.SIGKILL)
