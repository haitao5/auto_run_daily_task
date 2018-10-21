#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import re
import time
import logging
import aircv


def init_config():
    """ 初始配置
    
    """
    # 配置log输出格式
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s  -  %(message)s')
    # 切换到ADB文件夹下执行之后命令
    os.chdir(r".\adb")
    pass


class Terminal():
    def __init__(self):
        self.port_num = None
        self.screen_height = 0
        self.screen_width = 0
        pass

    def connect_to_terminal(self):
        """ 查找设备，检查环境配置
        """
        # 
        devices = os.popen('adb devices').read() 
        logging.debug('RUN: adb devices\n'+ devices) 

        port_num = '\n'.join(re.findall(r'^(\S+)\s+device', devices, re.M))
        logging.info('设备ID: ' + port_num)

        if not port_num:
            logging.critical('请安装 ADB 及驱动并配置环境变量')
            sys.exit()

        self.port_num = port_num
        return port_num

    def get_screen_size(self):   
        """ 获取屏幕尺寸
        """
        sizes = os.popen('adb shell wm size').read()
        logging.debug('RUN: adb shell wm size\n'+ sizes) 

        m = re.search(r'(\d+)x(\d+)', sizes)


        size = "{height}x{width}".format(height=m.group(2), width=m.group(1))
        logging.debug('屏幕尺寸: ' + size)

        self.screen_height = int(m.group(2))
        self.screen_width = int(m.group(1))
        return size

    def check_app(self, app):
        """ 查询APP
        """ 
        packages = os.popen('adb shell pm list packages').read()
        logging.debug('RUN: adb shell pm list packages\n'+ packages) 

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
        packages = os.popen('adb shell screencap -p /sdcard/screen.png').read()
        logging.debug('RUN: adb shell screencap -p /sdcard/screen.png\n' + packages) 

        packages = os.popen('adb pull /sdcard/screen.png .').read()
        logging.debug('RUN: adb pull /sdcard/screen.png .\n' + packages) 
        pass

    def swipe_screen(self, src, dest, timeout=10):
        """
        """
        cmd = "adb shell input swipe %d %d %d %d %d "  % (int(src[0]), int(src[1]), int(dest[0]), int(dest[1]), timeout)
        packages = os.popen(cmd).read()
        logging.debug('RUN: %s \n'%cmd + packages)        
        

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


    def find_obj(self, obj_img, timeout=5000):
        """  查找目标图标
        """
        pass


if __name__ == '__main__':
    init_config()

    t = Terminal()
    t.connect_to_terminal()
    t.get_screen_size()

    app = t.check_app('weibo')
    t.capture_screen()

    pos = t.compare_image('screen.png', '1.png')
    t.swipe_screen(pos, pos)


