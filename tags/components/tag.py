# coding:utf-8
import os
from freq import Keywords 
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("savefig", dpi=400)
from color import *



if __name__ == "__main__":
    d = os.path.abspath("..")
    file_path = "/home/zxingoo/supertags/tags/temp/tmp.txt"
    font_path = '/home/zxingoo/supertags/tags/material/fonts/FZLTKH.ttf'
    with open(file_path, 'r')as f:
        lines=f.readlines()
    text = ''.join(lines)
    txt_freq = Keywords(text).tf_idf()

    image_path = "/home/zxingoo/supertags/tags/material/shapes/pikachu.png"
    mask = np.array(Image.open(image_path))

    wc = WordCloud( font_path,#设置字体  
                    background_color="black", #背景颜色  
                    max_words=400,# 词云显示的最大词数  
                    mask=mask,#设置背景图片   
                    )  
    wc.generate_from_frequencies(txt_freq)  

    #plt.imshow(wc)
    plt.imshow(wc.recolor(color_func=image_colors_func(image_path)), interpolation="bilinear")
    #plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
    #       interpolation="bilinear")
    wc.to_file("/home/zxingoo/supertags/tags/temp/cartoon4.png")
    #plt.axis("off")
    #plt.savefig('/home/zxingoo/supertags/tags/temp/thumbs-up2.png',dpi = 400, bbox_inches="tight")
    # store default colored image

    
    
    
    
    
    
