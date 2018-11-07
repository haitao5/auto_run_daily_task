#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import re
import time
import logging
import aircv
import json
import unittest

def init_config():
    """ 初始配置
    
    """
    # 配置log输出格式
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s  -  %(message)s')
    # 切换到ADB文件夹下执行之后命令
    os.chdir(r".\adb")
    pass

def cleanup():
    """ 
    """
    # 删除截屏文件
    pass

class Terminal():
    def __init__(self):
        pass

    def __run_adb_cmd__(self, cmd):
        """ 执行ADB命令
        """
        if not isinstance(cmd, str):
            raise TypeError

        res = os.popen(cmd).read() 
        logging.debug('RUN: %s \n%s' %(cmd, res))
        return res

    def connect_to_terminal(self):
        """ 查找设备，检查环境配置
        """
        # 
        devices = self.__run_adb_cmd__('adb devices')

        port_num = '\n'.join(re.findall(r'^(\S+)\s+device', devices, re.M))
        logging.info('设备ID: ' + port_num)

        if not port_num:
            logging.critical('请安装 ADB 及驱动并配置环境变量')
            return None
        return port_num

    def get_screen_size(self):   
        """ 获取屏幕尺寸
        """
        sizes = self.__run_adb_cmd__('adb shell wm size')
        m = re.search(r'(\d+)x(\d+)', sizes)

        size = "{height}x{width}".format(height=m.group(2), width=m.group(1))
        logging.debug('屏幕尺寸: ' + size)

        return size

    def check_app(self, app):
        """ 查询APP
        """ 
        packages = self.__run_adb_cmd__('adb shell pm list packages')
        package = re.search(r"package:\S*%s"%app, packages)
        if not package:
            logging.critical('未查到目标APP！')
            sys.exit()

        app = package.group(0)
        logging.debug('匹配包: ' + str(app))
        return  app


    def capture_screen(self):
        """ 获取手机截屏，并保存到当前目录的screen.png
        """
        self.__run_adb_cmd__('adb shell screencap -p /sdcard/screen.png')
        self.__run_adb_cmd__('adb pull /sdcard/screen.png .')
        pass

    def swipe_screen(self, src, dest, timeout=10):
        """ 滑屏
        """
        cmd = "adb shell input swipe %d %d %d %d %d "  % (int(src[0]), int(src[1]), int(dest[0]), int(dest[1]), timeout)   
        return self.__run_adb_cmd__(cmd)  

    def compare_image(self, src_img, obj_img):
        """" 查找并返回 obj_img 图像在 src_img 图像的位置
        """
        im_src = aircv.imread(src_img)  
        im_obj = aircv.imread(obj_img)

        pos = aircv.find_template(im_src, im_obj)
        logging.debug('Compare_Image: \nSource Image: %s \nObject Image:%s \nResults: %s\n' %(src_img, obj_img, pos)) 
        
        if pos:
            return pos['result']
        else:
            return None


    def find_obj(self, obj_img, timeout=5):
        """  查找目标图标
        """
        start_time = time.time()
        current_time = start_time

        while current_time - start_time < timeout:
            pass

        pass


class TestDaiyTask(unittest.TestCase):
    """
    """
    def setUp(self):
        init_config()

    def test_weibo(self):
        task_name = 'weibo'

        t = Terminal()
        port = t.connect_to_terminal()
        self.assertIsNotNone(port)

        size = t.get_screen_size()
        path =  '../Config/' + task_name + '/' + size + '/'

        app = t.check_app(task_name)
        self.assertIsNotNone(app)

        with open(path+task_name + '.json', 'r') as f:
            config = json.load(f)

        for i in range(1, config["step_num"]+1):
            current_step = config["step%d"%i] 

            for loop in range(current_step["loop_count"]):
                logging.debug('Current Step: %s,    Current Loop: %d\n' %(current_step, loop)) 
       
                t.capture_screen()
                pos = t.compare_image('screen.png', path+current_step["templ_icon"])

                if current_step["swip_find_need"] and not pos:
                    t.swipe_screen((300,1000), (300,300), 1000)
                    t.capture_screen()
                    pos = t.compare_image('screen.png', path+current_step["templ_icon"])
                
                if pos:
                    t.swipe_screen(pos, pos)
                
                time.sleep(current_step["delay_after_process"])

    def test_taobao(self):
        task_name = 'taobao'

        t = Terminal()
        port = t.connect_to_terminal()
        self.assertIsNotNone(port)

        size = t.get_screen_size()
        path =  '../Config/' + task_name + '/' + size + '/'

        app = t.check_app(task_name)
        self.assertIsNotNone(app)

        with open(path+task_name + '.json', 'r') as f:
            config = json.load(f)

        for i in range(1, config["step_num"]+1):
            current_step = config["step%d"%i] 

            for loop in range(current_step["loop_count"]):
                logging.debug('Current Step: %s,    Current Loop: %d\n' %(current_step, loop)) 
       
                t.capture_screen()
                pos = t.compare_image('screen.png', path+current_step["templ_icon"])

                if current_step["swip_find_need"] and not pos:
                    t.swipe_screen((300,1000), (300,300), 1000)
                    t.capture_screen()
                    pos = t.compare_image('screen.png', path+current_step["templ_icon"])
                
                if pos:
                    t.swipe_screen(pos, pos)
                
                time.sleep(current_step["delay_after_process"])

if __name__ == '__main__':
    unittest.main()



