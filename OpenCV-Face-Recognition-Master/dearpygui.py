from dearpygui.core import *
from dearpygui.simple import *

def check_spam(sender,data,pred=[]):
    with window("Simple SMS Spam Filter"):
        if pred == []:
            input_value = get_value("Input")
            pred.append(input_value)
            print("Scenario 1"+ input_value)
        else:
            input_value = get_value("Input")
            pred.append(input_value)
            print("Scenario 2" + input_value)


 #Window object setting
set_main_window_size(540,720)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30,30)

with window("Simple SMS Spam Filter", width = 520, height = 677):
    print("GUI is Running....")
    set_window_pos("Simple SMS Spam Filter",0,0)

    #LOGO
    add_drawing("logo",width=520,height=290)
    add_separator()
    add_spacing(count=12)

    #Instructions
    add_text("Please Enter SMS:",
             color =[232,163,33])
    add_spacing(count=12)

    #Collect Input
    add_input_text("Input", width=415 , default_value= "Type Message Here")
    add_spacing(count=12)
    add_button("Check",callback= check_spam)

draw_image("logo", "101-1018555_checking-attendance-comments-attendance-icon-transparent-clipart.png",[0,5],[290,290])
start_dearpygui()
