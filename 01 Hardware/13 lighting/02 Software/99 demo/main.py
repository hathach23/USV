# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

from machine import Pin 
from button_handle import ButtonHandler
from state_machine import StateMachine
from user_state_functions import *
from hardware import BUTTON_PINS


# Function for initialization
def initialize():
    button_handler = ButtonHandler(BUTTON_PINS)
    state_machine = StateMachine()
    return button_handler, state_machine

# Dictionary with all State-Functions
state_functions = {
    1: s_f_1,
    2: s_f_2,
    3: s_f_3,
    4: s_f_4,
    5: s_f_5,
    6: s_f_6,
    7: s_f_7,
    8: s_f_8,
    9: s_f_9,
    10: s_f_10,
    11: s_f_11,
}

# Main loop
button_handler, state_machine = initialize()
current_state = 1  # Start State (PROCESS)
s_f_1()  # User-State PROCESS

while True:
    if (button_handler.button_click != 0) or (alarm_state() == 0):  # Button Click or timer == 0
        current_state = state_machine.transition(current_state, 11, int(button_handler.button_click), alarm_state())  # Trigger State-machine  
        
        if current_state in state_functions:  # Call User-State-Function
            state_functions[current_state]()
        else:
            print("State not defined")

        button_handler.button_click = 0  # Reset Button
