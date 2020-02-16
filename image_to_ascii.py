"""
Image to ASCII

Description: Accepts image file of type .jpg, .png. Converts image to array of ascii characters based on the amount of
white and black space.

Author: Nic La
Last modified: Feb 2020
"""

from PIL import Image
import numpy as np

np.set_printoptions(threshold=np.nan)   # prints all char

image_file = 'input.png'
const_white_filter = 1  # 100/(max white content in char), filter constant to better fit white content in ascii_table
const_black_filter = 2.86  # 100/(max black content in char), filter constant to better fit black in ascii_table


# accepts a (black, white) and returns the a best fit char
def best_fit_ascii(black, white):
    # dict consisting of char, (black %, white %)
    ascii_table = {'1': (22, 78), '2': (23, 77), '3': (22, 78), '4': (27, 73),
                   '5': (23, 77), '6': (27, 73), '7': (19, 81), '8': (32, 68),
                   '9': (27, 73), '0': (33, 67), ',': (8, 92), '!': (13, 87),
                   'A': (29, 71), 'B': (33, 67), 'C': (21, 79), 'D': (31, 69),
                   'E': (26, 74), 'F': (21, 79), 'G': (29, 71), 'H': (21, 71),
                   'I': (22, 78), 'J': (20, 80), 'K': (26, 74), 'L': (17, 83),
                   'M': (33, 67), 'N': (33, 67), 'O': (29, 71), 'P': (25, 75),
                   'Q': (35, 65), 'R': (30, 70), 'S': (24, 76), 'T': (19, 81),
                   'U': (27, 73), 'V': (25, 75), 'W': (33, 67), 'X': (27, 73),
                   'Y': (21, 79), 'Z': (26, 74), ' ': (0, 100), '.': (5, 95)}

    prev_dif = 201

    # compare input(black) against char(black), input(white) against char(white)
    # return char with lowest difference
    for key, val in ascii_table.items():
        black_dif = abs(black - val[0])
        white_dif = abs(white - val[1])
        total_dif = black_dif + white_dif
        if total_dif <= prev_dif:
            chosen_char = key
            prev_dif = total_dif

    return chosen_char


# opens an image and returns an array of (black, white) ints
def image_to_array(image_name):
    im = Image.open(image_name)
    im_array = np.asarray(im)       # creates an array of (height, width) of RGB values, one for each pixel
    # DEBUG: print(im_array)

    # convert a (255, 255, 255) array to (black, white) array
    # 255 + 255 + 255 = 765 = percent_white
    num_array = []
    for a in range(len(im_array)):
        num_array.append([])
        for b in range(len(im_array[a])):
            # num_array[a].append(int(im_array[a][b]) + int(im_array[a][b]) + int(im_array[a][b]))
            num_array[a].append(int(im_array[a][b][0]) + int(im_array[a][b][1]) + int(im_array[a][b][2]))
    return num_array


# Main Function
if __name__ == '__main__':
    num_array = image_to_array(image_file)

    ascii_array = []
    for count, x in enumerate(num_array):
        ascii_array.append([])
        for y in x:
            white = int((y / 765) * 100) / const_white_filter  # converts white content to a percentage
            black = (100 - white) / const_black_filter  # converts black content to a percentage
            ascii_array[count].append(best_fit_ascii(black, white))

    text_file = open('output.txt', 'w')
    for a in ascii_array:
        for b in a:
            text_file.write(b)
        text_file.write('\n')
    text_file.close()

    # DEBUG: determine white percentage of image
    # total_white = 0
    # for count, x in enumerate(num_array):
    #     total_white += sum(num_array[count])
    # print((total_white / (765*10000)) * 100)

'''
                                        ..        
                                   ..,,...,       
                                .,. .... ,.       
                               ,....... .,        
                    .        .! ., .....L,        
                   !.      .,,....!.  ,,.,        
            .,.     !!,.  !,  ,...   ...,         
             .D.     .LQZX, ..,....,  ..          
              ,IWDLTTL!STT!!L,........            
    .,..  ..   LDWQ8XDWQQQQQQQQDIITLLT!.          
        ..,!SQQQXXWDWXOQQQQQQQQQQQQXSSVOW5,       
           RQQQQXSSTOXIXQQQQQQQQQQQXSSIVQQQW.     
          ,QQQQQDS5TXRS5QQQQQQQQQQQZ!!!LQQQQQL    
   .,,,,,,,,!QQQQQW5SZVVXQQQQQQQQQQQT,,LWQQQXDS   
              .,!,XQWRD5JX!.......,!,..,LRQWYJO   
               ,LRRLJIDQQQQO!..,....,,...,,!LIJ   
            ,LLL!,     ,TDQQQ8,.,,. .......!,J.   
          LXV!            XWL..,,. .  ... ..L.    
        .J.               .WY    ,,. ...  ..,T.   
                          LQL      ....... . ,!   
                         .QZ.            ....,.   
                          I                       
                          .                                                                    
'''
