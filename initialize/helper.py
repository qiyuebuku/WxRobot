<<<<<<< HEAD




# class Robot_management(Thread):
#     """
#     机器人管理者，管理活动的机器人，当机器人对象超出预先设定好的走向时，杀死他::
#         * 如果一个机器人的存活时间超过了预设的值，程序将会检测他是否被用户登录。
#         * 如果不是，这个机器人线程将会被清理掉。
#     """
#     def __init__(self,*,qr_timeout=20,inspection_interval=5):
#         """ 
#         :parqr_timeout:
#             * 设定未被扫码的持续时间
#             * 单位为秒
#         :param inspecition_interval
#             * 检测间隔
#             * 多少秒进行一次检测

#         """
#         super().__init__()
#         self.bot_thread = {}
#         self.qr_timeout = qr_timeout
#         self.inspection_interval=inspection_interval 
#         # self.has_logged = {}

#     def run(self):
#         while True:
#             bot_thread = self.bot_thread
#             Current_timestamp = int(time.time()) 
#             # 待清理的二维码id
#             cleaner_uuid = [] 
#             if not len(bot_thread.values()):
#                 continue
#             for uuid in bot_thread:
#                 # 将超过了超时时间的二维码加入到待清理列表，准备销毁
#                 if bot_thread[uuid]['time']+self.qr_timeout<Current_timestamp:
#                     try:
#                         if bot_thread[uuid]['object'].bot.alive:
#                             # 如果机器人为登录状态，则跳过
#                             continue
#                     except AttributeError:
#                         debug.print_l('二维码被创建时间',bot_thread[uuid]['time'])
#                         debug.print_l('当前时间：',Current_timestamp)
#                         cleaner_uuid.append(uuid)  
#             # 将待处理列表里的二维码销毁
#             for uuid in cleaner_uuid: 
#                 if self.cleaner(uuid)<0:
#                    debug.print_l('二维码id：%s存在抵抗行为，自动清理失败！！！'%uuid)
#                    continue
#                 debug.print_l('二维码ID：%s,清理完成'%uuid)
#             debug.print_l('---------------------------------------')
#             debug.print_l('当前活动二维码：',self.bot_thread)
#             debug.print_l('---------------------------------------')


#             # for i in self.has_logged:

#             time.sleep(self.inspection_interval)
    
#     # 二维码清理器
#     def cleaner(self,bot_uuid): 
#         '''
#             功能：用于强制结束一个线程的执行
#             bot_uuid：需要被清理的机器人uuid
#         '''
#         try:
#             thread = self.bot_thread[bot_uuid]['object']   # 获取线程对象
#             # 如果二维码在被登录时出现了问题，就直接删除！！！
#             if not thread.bot_status:
#                 del self.bot_thread[bot_uuid] # 从监控列表中移除
#                 return True
#             # 要删除的线程必须是活动线程，否则直接从字典里面移除
#             try:
#                 self._async_raise(thread.ident,SystemExit)  #终止二维码线程
#             except:
#                 pass 
#             del self.bot_thread[bot_uuid] # 从监控列表中移除
#             return True
#         except Exception as e:
#             print(e)
#             return False

#     # 用于强制终止线程的运行
#     def _async_raise(self,tid,exctype):
#         '''
#             tid : 线程的识别符
#             exctype : 类型，如：SystemExit，表示终止这个线程
#         '''

#         """raises the exception, performs cleanup if needed"""
#         tid = ctypes.c_long(tid)
#         if not inspect.isclass(exctype):
#             exctype = type(exctype)
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#         if res == 0:
#             raise ValueError("invalid thread id")
#         elif res != 1:
#             # """if it returns a number greater than one, you're in trouble,
#             # and you should call it again with exc=NULL to revert the effect"""
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#             raise SystemError("PyThreadState_SetAsyncExc failed")

#     # 增加需要被管理的机器人
#     def add(self,bot_uuid,bot_object):
#         """
#             用于将需要被管理的机器人线程加入进来
#             :param bot_uuid 
#                 * 机器人的uuid号
#             :param bot_object
#                 * 机器人对应的线程对象
#         """
#         # 获取当前的时间戳
#         Current_timestamp = int(time.time()) 
#         self.bot_thread[bot_uuid]={'object':bot_object,'time':Current_timestamp}

# # 创建管理线程
# rmt = Robot_management(qr_timeout=60)
# # 主进程退出，线程也跟着陪葬
# rmt.setDaemon(True)
# rmt.start()











=======




# class Robot_management(Thread):
#     """
#     机器人管理者，管理活动的机器人，当机器人对象超出预先设定好的走向时，杀死他::
#         * 如果一个机器人的存活时间超过了预设的值，程序将会检测他是否被用户登录。
#         * 如果不是，这个机器人线程将会被清理掉。
#     """
#     def __init__(self,*,qr_timeout=20,inspection_interval=5):
#         """ 
#         :parqr_timeout:
#             * 设定未被扫码的持续时间
#             * 单位为秒
#         :param inspecition_interval
#             * 检测间隔
#             * 多少秒进行一次检测

#         """
#         super().__init__()
#         self.bot_thread = {}
#         self.qr_timeout = qr_timeout
#         self.inspection_interval=inspection_interval 
#         # self.has_logged = {}

#     def run(self):
#         while True:
#             bot_thread = self.bot_thread
#             Current_timestamp = int(time.time()) 
#             # 待清理的二维码id
#             cleaner_uuid = [] 
#             if not len(bot_thread.values()):
#                 continue
#             for uuid in bot_thread:
#                 # 将超过了超时时间的二维码加入到待清理列表，准备销毁
#                 if bot_thread[uuid]['time']+self.qr_timeout<Current_timestamp:
#                     try:
#                         if bot_thread[uuid]['object'].bot.alive:
#                             # 如果机器人为登录状态，则跳过
#                             continue
#                     except AttributeError:
#                         debug.print_l('二维码被创建时间',bot_thread[uuid]['time'])
#                         debug.print_l('当前时间：',Current_timestamp)
#                         cleaner_uuid.append(uuid)  
#             # 将待处理列表里的二维码销毁
#             for uuid in cleaner_uuid: 
#                 if self.cleaner(uuid)<0:
#                    debug.print_l('二维码id：%s存在抵抗行为，自动清理失败！！！'%uuid)
#                    continue
#                 debug.print_l('二维码ID：%s,清理完成'%uuid)
#             debug.print_l('---------------------------------------')
#             debug.print_l('当前活动二维码：',self.bot_thread)
#             debug.print_l('---------------------------------------')


#             # for i in self.has_logged:

#             time.sleep(self.inspection_interval)
    
#     # 二维码清理器
#     def cleaner(self,bot_uuid): 
#         '''
#             功能：用于强制结束一个线程的执行
#             bot_uuid：需要被清理的机器人uuid
#         '''
#         try:
#             thread = self.bot_thread[bot_uuid]['object']   # 获取线程对象
#             # 如果二维码在被登录时出现了问题，就直接删除！！！
#             if not thread.bot_status:
#                 del self.bot_thread[bot_uuid] # 从监控列表中移除
#                 return True
#             # 要删除的线程必须是活动线程，否则直接从字典里面移除
#             try:
#                 self._async_raise(thread.ident,SystemExit)  #终止二维码线程
#             except:
#                 pass 
#             del self.bot_thread[bot_uuid] # 从监控列表中移除
#             return True
#         except Exception as e:
#             print(e)
#             return False

#     # 用于强制终止线程的运行
#     def _async_raise(self,tid,exctype):
#         '''
#             tid : 线程的识别符
#             exctype : 类型，如：SystemExit，表示终止这个线程
#         '''

#         """raises the exception, performs cleanup if needed"""
#         tid = ctypes.c_long(tid)
#         if not inspect.isclass(exctype):
#             exctype = type(exctype)
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#         if res == 0:
#             raise ValueError("invalid thread id")
#         elif res != 1:
#             # """if it returns a number greater than one, you're in trouble,
#             # and you should call it again with exc=NULL to revert the effect"""
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#             raise SystemError("PyThreadState_SetAsyncExc failed")

#     # 增加需要被管理的机器人
#     def add(self,bot_uuid,bot_object):
#         """
#             用于将需要被管理的机器人线程加入进来
#             :param bot_uuid 
#                 * 机器人的uuid号
#             :param bot_object
#                 * 机器人对应的线程对象
#         """
#         # 获取当前的时间戳
#         Current_timestamp = int(time.time()) 
#         self.bot_thread[bot_uuid]={'object':bot_object,'time':Current_timestamp}

# # 创建管理线程
# rmt = Robot_management(qr_timeout=60)
# # 主进程退出，线程也跟着陪葬
# rmt.setDaemon(True)
# rmt.start()











>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
