import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from modules.logger import CustomLogger
from modules.testclass import TestClass

class Script():

    def __init__(self):

        nlog = CustomLogger()
        nlog.setLevel(1)
        nlog.trace(f"Trace Testing")
        nlog.info(f"Testing {1}")
        TestClass()
Script()
