import inspect
import ctypes

class Debug(object):
    def __init__(self,flag):
        self.debug=flag 

    def print_l(self,*args,**kwargs):
        if self.debug:
            print(*args,**kwargs)

    def kill_thread(self,thread_id):
        """
        ：params　需要被结束的线程对象
        """
        if not type(thread_id) == int:
            thread_id = thread_id.ident
        try:
            self._async_raise(thread_id,SystemExit)  #终止定时发送线程
        except Exception as e:
            print('强制结束失败：',e)

    # 用于强制终止线程的运行
    def _async_raise(self,tid,exctype):
        '''
            tid : 线程的识别符
            exctype : 类型，如：SystemExit，表示终止这个线程
        '''

        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

debug = Debug(True)





    