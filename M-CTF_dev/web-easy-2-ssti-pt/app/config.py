import os, re

class Config(object):
    DEBUG = False
    SECRET_KEY = 'r1v3n_1s_th3_b3st_g1rl'
    FLAG = os.environ['FLAG']


class Disabled(object):
    def __init__(self, string, blocked=None, aborted=None):
        self.string = string
        self.blocked = blocked
        self.aborted = aborted

    def check_blocked(self) -> bool:
        sub = re.findall(r'conf*.*', str(self.string))
        if len(sub) != 0:
            self.blocked = True
        else:
            self.blocked = False
        return self.blocked

    def abort_rq(self) -> bool:
        sub = re.findall(r'server*', str(self.string))
        if len(sub) != 0:
            self.aborted = True
        else:
            self.aborted = False
        return self.aborted

