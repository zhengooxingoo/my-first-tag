from PIL import Image,ImageOps
import numpy as np
import random
from wordcloud import ImageColorGenerator,get_single_color_func
from colored_by_group import (SimpleGroupedColorFunc,GroupedColorFunc)

'''
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
'''

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


# store default colored image
def default_colors_func(wc):
    return  wc.to_array()


'''
plt.imshow(wc.recolor(color_func=image_colors_func), interpolation="bilinear")
'''
# create coloring from image
def image_colors_func(image_path):
    image_coloring = np.array(Image.open(image_path))
    return ImageColorGenerator(image_coloring)


'''
color_to_words = {
    # words below will be colored with a green single color function
    '#00ff00': ['beautiful', 'explicit', 'simple', 'sparse',
                'readability', 'rules', 'practicality',
                'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # will be colored with a red single color function
    'red': ['ugly', 'implicit', 'complex', 'complicated', 'nested',
            'dense', 'special', 'errors', 'silently', 'ambiguity',
            'guess', 'hard']
}
default_color = 'grey'
# Create a color function with single tone
grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
# Create a color function with multiple tones
grouped_color_func = GroupedColorFunc(color_to_words, default_color)
'''
# Create a color function with single tone
def single_group_colors_func(color_to_words, default_color):
    return SimpleGroupedColorFunc(color_to_words, default_color)

# Create a color function with multiple tones
def multi_group_colors_func(color_to_words, default_color):
    return GroupedColorFunc(color_to_words, default_color)




if __name__ == "__main__":
    pass
