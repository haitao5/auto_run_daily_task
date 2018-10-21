#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import re
import time
import logging

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

    def compare_picture(self, image, template):
        """" 查找并返回template图像在image图像的位置
        """

        pass


              



if __name__ == '__main__':
    init_config()

    t = Terminal()
    t.connect_to_terminal()
    t.get_screen_size()

    app = t.check_app('weibo')
    t.capture_screen()



