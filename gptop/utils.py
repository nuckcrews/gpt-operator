def announce(val, prefix: str=""):
    cyan = '\033[96m'
    default = '\033[0m'
    print("{0}{1}{2}{3}".format( prefix, cyan, val, default))