from os import path as ospath
from sys import path as syspath
from logging import getLogger

syspath.insert(0, ospath.dirname(ospath.realpath(__file__)))
from logger import CustomLogger

class TestClass():

    def __init__(self):
        #Setup logging.
        if __name__ == "__main__":
            nlog = CustomLogger()
        else:
            nlog = getLogger(__name__)

        #Set per-module logging level.
        nlog.setLevel(20)

        nlog.trace("testclass - Trace Log")
        nlog.info("testclass.py - Info Log")
        nlog.warning("testclass.py - Warning Log")
