# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:00:20 2023

@author: Joe Grabow (grabow@amesys.de)


The state machine changes its state depending on the input. 
If no input matches, it does not change its state.
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

class StateMachine:
    def __init__(self):
        self.state = 1  # default

    # in_state  : current state
    # item      : Menue-Item 
    # input_sw  : Up=1, ENTER=2, DOWN=3
    # timer     : Process timer
    def transition(self, in_state, item, input_sw, timer):
        if in_state == 1 and item == 11 and input_sw == 2:
            self.state = 2                              # --> DEV-Timer init
        elif in_state == 2 and input_sw == 1:           # go state 1
            self.state = 1                              # --> PROCESS
        elif in_state == 2 and input_sw == 2:           # go state 3
            self.state = 3                              # --> DEV-Timer run
        elif in_state == 3 and input_sw == 1:           # go state 2
            self.state = 2                              # --> DEV-Timer init
        elif in_state == 3 and input_sw == 2:           # go state 4
            self.state = 4                              # --> DEV-Timer wait
        elif in_state == 4 and input_sw == 1:           # go state 2
            self.state = 2                              # --> DEV-Timer init
        elif in_state == 4 and input_sw == 2:           # go state 3
            self.state = 3                              # --> DEV-Timer run
        elif (in_state == 3 and timer == 0) or (in_state == 3 and input_sw == 3):  # go state 5
            self.state = 5                              # --> STOP-Timer init
        elif in_state == 5 and input_sw == 1:           # go state 2    
            self.state = 2                              # --> DEV-Timer init
        elif in_state == 5 and input_sw == 2:           # go state 6
            self.state = 6                              # --> STOP-Timer run
        elif in_state == 6 and input_sw == 1:           # go state 5    
            self.state = 5                              # --> STOP-Timer init
        elif in_state == 6 and input_sw == 2:           # go state 7
            self.state = 7                              # --> STOP-Timer wait
        elif in_state == 7 and input_sw == 1:           # go state 5
            self.state = 5                              # --> STOP-Timer init
        elif in_state == 7 and input_sw == 2:           # go state 6
            self.state = 6                              # --> STOP-Timer run
        elif  (in_state == 6 and timer == 0) or (in_state == 6 and input_sw == 3):  # go state 8
            self.state = 8                              # --> FIX-Timer init
        elif in_state == 8 and input_sw == 1:           # go state 5
            self.state = 5                              # --> STOP-Timer init
        elif in_state == 8 and input_sw == 2:           # go state 9 
            self.state = 9                              # --> FIX-Timer run
        elif in_state == 9 and input_sw == 1:           # go state 8
            self.state = 8                              # --> FIX-Timer init
        elif in_state == 9 and input_sw == 2:           # go state 10
            self.state = 10                             # --> FIX-Timer wait
        elif in_state == 10 and input_sw == 1:          # go state 8
            self.state = 8                              # --> FIX-Timer init
        elif in_state == 10 and input_sw == 2:          # go state 9
            self.state = 9                              # --> FIX-Timer run
        elif  (in_state == 9 and timer == 0) or (in_state == 9 and input_sw == 3):  # go state 11
            self.state = 11                             # --> PROCESS end
        elif in_state == 11 and input_sw == 1:          # go state 8
            self.state = 8                              # --> FIX-Timer init
        elif in_state == 11 and input_sw == 2:          # go state 1
            self.state = 1                              # --> PROCESS
        else:
            self.state = self.state                     # old state = new state
        return self.state
