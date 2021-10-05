How to add the logging function to all modules.

    class Example():

        def __init__(self):
            #Setup logging.
            if __name__ == "__main__":
                nlog = CustomLogger()
            else:
                nlog = getLogger(__name__)

            #Set per-module logging level.
            nlog.setLevel(20)
