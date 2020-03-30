import getopt
import os
import sys
import time

import config
from hkws import *

# 启动函数  python3 main.py -c xxx/xxx

# ==================sdk加载===========start================
cnfPath = ''
opts, args = getopt.getopt(sys.argv[1:], '-c:')
for opt_name, opt_val in opts:
    if opt_name in '-c':
        cnfPath = opt_val

if cnfPath == '':
    print('Please enter the config path.')

# 初始化配置文件
cnf = config.Config()
path = os.path.join(cnfPath, 'local_config.ini')
cnf.InitConfig(path)

# 初始化基础SDK适配器
adapter = base_adapter.BaseAdapter()
adapter.add_lib(cnf.SDKPath, cnf.suffix)
print(adapter.so_list)

# 设置sdk路径，海康威视系统环境配置异常时使用
# adapter.set_sdk_config(2, cnfPath)

# 基础适配器=>加载sdk到内存
initRes = adapter.init_sdk()
if initRes is False:
    os._exit(0)

# ==================sdk加载===========end================


# ==================设备用户登录===========start================
# 基础适配器=>设备用户登录
userId = adapter.login(cnf.IP, cnf.Port, cnf.User, cnf.Password)
if userId < 0:
    adapter.sdk_clean()
    os._exit(1)
# ==================设备用户登录===========end================


# ==================图像类适配器操作===========start================
caremaAdpt = cm_camera_adpt.CameraAdapter(adapter)

#set_dvr_config = adapter.set_dvr_config(userId)
#print("设置设备信息结果为 ", set_dvr_config)
#data = adapter.setup_alarm_chan_v31(cb.face_alarm_call_back, userId)
#print("设置回调函数结果", data)
# 布防
#alarm_result = adapter.setup_alarm_chan_v41(userId)
#print("设置人脸v41布防结果", alarm_result)

lRealPlayHandle = caremaAdpt.start_preview(None, userId)
if lRealPlayHandle < 0:
     os._exit(2)

print("Start preview successful,the lRealPlayHandle is ", lRealPlayHandle)
callback = caremaAdpt.callback_real_data(lRealPlayHandle, callback.g_real_data_call_back, userId)
print('callback_real_data result is ', callback)
time.sleep(20)


#adapter.close_alarm(alarm_result)
caremaAdpt.stop_preview(lRealPlayHandle)

# ==================图像类适配器操作===========start================


adapter.logout(userId)
adapter.sdk_clean()
