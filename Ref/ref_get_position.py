"""
--------------------- 
作者：Immok 
来源：CSDN 
原文：https://blog.csdn.net/ns2250225/article/details/60334176 
版权声明：本文为博主原创文章，转载请附上博文链接！
"""

import cv2
import aircv as ac

# print circle_center_pos
def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    imsrc = ac.imread('bg.jpg')
    #imobj = ac.imread('obj.png')    
    imobj = ac.imread('obj2.png')


    # find the match position
    pos = ac.find_template(imsrc, imobj)

    circle_center_pos = (int(pos['result'][0]), int(pos['result'][1]))
    print(circle_center_pos)
    circle_radius = 50
    color = (0, 255, 0)
    line_width = 10

    # draw circle
    draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)
