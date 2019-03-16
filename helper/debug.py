class Debug(object):
    def __init__(self,flag):
        self.debug=flag 

    def print_l(self,*args,**kwargs):
        if self.debug:
            print(*args,**kwargs)

debug = Debug(True)