
root = "that"
passwd = "those"

class Accessor:
    """This class accesses the MySQL database"""
    def __init__(self, root, passwd):
        self.root = root
        self.passwd = passwd
    def test(self, string):
        return string