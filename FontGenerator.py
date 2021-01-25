import os
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from PIL import ImageFont, Image, ImageDraw
import numpy as np
from scipy.signal.signaltools import correlate2d as c2d

font = 'tahomabd.ttf'

# Function To normalize the Original Pic and the Generated image
def get(data):
    data = np.array(data)
    return (data - data.mean()) / data.std()


# The name of Books/Magazines
image_folders_names = ['abwab', 'adab el rafydan', 'afaq arabya', 'el adib', 'el doha', 'el helal', 'el mnar','el qesa']
image_names = [];text_names = []
pathImage = "C:/Users/Yusuf/Desktop/RDI Data/test_data/words_images_new/"
pathText = "C:/Users/Yusuf/Desktop/RDI Data/test_data/words_text/"

# getting all Text and Photo names from the given directoryy
for i, name in enumerate(image_folders_names):
    image_names.append([]);
    text_names.append([])
    for photo_name in os.listdir(pathImage + name):
        image_names[i].append(photo_name)
        text_names[i].append(photo_name[:-3] + 'txt')

# Compare using CrossCorrelation
count = 0
Threshold = 881.332419688
matched_font = None
mismatched = []
matched_img = None
# plt.figure(figsize=(100,100))
for f_idx in range(len(image_folders_names)):
    #What's the mismatched photos for this folder
    mismatched.append([])
    for j, pic_name in enumerate(image_names[f_idx]):
        orig = Image.open(pathImage + image_folders_names[f_idx] + '/' + pic_name)
        txt_file = open(pathText + image_folders_names[f_idx] + '/' + text_names[f_idx][j], encoding='utf-8')
        txt_file = txt_file.read()

        # know size of text image
        reshaped_text = arabic_reshaper.reshape(txt_file)
        bidi_text = get_display(reshaped_text)
        fnt = ImageFont.truetype(font=font, size=55)
        font_size = fnt.getsize(bidi_text)
        # make a blank image
        img = Image.new('L', (font_size[0], font_size[1]), (255))
        # draw the text into the blank image
        d = ImageDraw.Draw(img)
        d.text((0, 0), text=bidi_text, fill=(0), font=fnt)
        #cross correlation
        c = c2d(get(img), get(orig), mode='same')
        if (c.max() < Threshold):
            print(c.max(),pic_name)
            mismatched[f_idx].append(pic_name)

    print('the mismatched photos names for the folder :' + str(image_folders_names[f_idx])+'are')
    print(mismatched[f_idx])

#Many of the mismatched photos are because of the Symbols (ex: (.) ) or the photo isn't cropped well
#Following is some of these mismatechd photos with its maximum value of 2DCorrleation
# 572.258142324 Abwab_Abwab_book_abwab_abwab_1998_issue_17_136_Line14_w1.bmp
# 694.502989887 Abwab_Abwab_book_abwab_abwab_1998_issue_17_136_Line20_w5.bmp
# 619.243963068 Abwab_Abwab_book_abwab_abwab_1994_issue_1_107_Line12_w16.bmp
# 567.822650153 Abwab_Abwab_book_abwab_abwab_1994_issue_1_107_Line12_w6.bmp
# 582.617044898 Abwab_Abwab_book_abwab_abwab_1997_issue_12_148_Line23_w6.bmp
# 379.392065227 Abwab_Abwab_book_abwab_abwab_1998_issue_17_136_Line12_w0.bmp
# 453.948913507 EL_qesa_book_al_arabi_al_arabi_1961_issue_26_068_Line37_w6.bmp
# 843.958251877 EL_qesa_book_al_arabi_al_arabi_1961_issue_26_068_Line63_w0.bmp
# 610.333329028 EL_qesa_book_al_arabi_al_arabi_1961_issue_26_068_Line63_w4.bmp
# 798.87443925 EL_qesa_book_al_arabi_al_arabi_1961_issue_26_068_Line74_w3.bmp
# 861.566020036 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line10_w5.bmp
# 822.28539964 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line14_w3.bmp
# 266.190790957 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line14_w6.bmp
# 166.414639687 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line17_w6.bmp
# 335.921338433 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line19_w11.bmp
# 776.865611834 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line19_w3.bmp
# 147.172071818 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line20_w7.bmp
# 741.91885621 EL_qesa_book_al_arabi_al_arabi_1961_issue_37_065_Line25_w3.bmp