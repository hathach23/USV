"""
Created on Wed Oct 16 13:37:32 2024
SBUS.py
@author: Joe Grabow
https://github.com/Joe-Grabow/USV

Liest immer ein Byte von der seriellen Schnittstelle ein und löst damm Interrupt aus.
Im Interrupt-Handler werden 50 Byte in einen Puffer eingelesen. Ist der Puffer voll, wird er
auf full gesetzt. In der main kann auf full abgefragt werden, um dann mit der Dekodierung
zu beginnen.
"""

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
import utime

__version__ = '1.0'
__author__ = 'Joe Grabow'

# --- PIO-RX ---
#
# 8E2 (9 Bit) Receiver, even wird hier nicht geprüft!
# prüft das Startbit 2x, das 1. Stopbit und 2. Stopbit nur einmal
# Die Datenbits werden jeweils 1x in der Bitmitte abgetastet.
# PIO_Takt = Baud * 9
# 8 Bits werden von rechts eingeschoben (LSB first)
@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, fifo_join=rp2.PIO.JOIN_RX)
def uart_rx():
    label("restart")    
    wrap_target()             # Begin Schleife der Statemachine
    
    wait(1, pin, 0)           # wartet auf steigende Flanke (Startbit)
    mov(isr, null)            # bei Fehler ISR zurücksetzen
    set(y, 7)                 # Bit-Counter auf 8 Bit (8E) setzen

    jmp(pin, "start") [1]     # 4. Takt das Startbit ist noch high
    jmp("restart")            # ansonsten Fehler

    label ("start")
    jmp(pin, "nextbit") [7]   # 6. Takt das Startbit ist noch high
    jmp("restart")            # Fehler


                              # warten bis die Bit-Mitte des 1. Bits erreicht ist
                              # vom Start aus 9 + 5  = 14 Takte um sind
                              # 1 + 1 + 1 + (1 + 1) +  (1 + 8) = 14 Takte
    label("nextbit")
    in_(pins, 1) [7]          # GPIO einlesen und ein Bit in das Input Shiftregister
    jmp(y_dec, "nextbit")     # nach genau 10 Takten nächstes Bit einlesen

    nop() [8]                 # Paritätsbit überspringen
    
    jmp(pin,"restart") [8]    # wenn 1. Stopbit high, Fehler
    jmp(pin,"restart")        # wenn 2. Stopbit high, Fehler

    in_(null, 24)             # 24 Nullen nachschieben
    push()                    # die empfangenen 8 Bits ins Fifo
    irq(rel(0))               # Interrupt sofort ohne Verzögerung auslösen, rel(0)
    wrap()                    # End Schleife Statemachine 



# --- Datenpuffer ---
class DataBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = bytearray(size)
        self.index = 0
        self.full = False

    def put(self, value):
        if self.index < self.size:
            self.buffer[self.index] = value
            self.index += 1
        if self.index >= self.size:
            self.full = True

    def reset(self):
        self.index = 0
        self.full = False

    def is_full(self):
        return self.full

    def get_all(self):
        return self.buffer[:self.index]

# --- UART Receiver-Klasse ---
class UART_RX:
    def __init__(self, statemachine, rx_pin, baud=100000):
        self.sm = StateMachine(statemachine, uart_rx,
                               in_base=Pin(rx_pin, Pin.IN, Pin.PULL_DOWN),
                               jmp_pin=Pin(rx_pin, Pin.IN, Pin.PULL_DOWN),
                               freq=baud * 9)
        self.buffer = DataBuffer(50)  # minimale Puffergröße
        self.sm.irq(self.irq_handler)
        self.interrupt_locked = False

    def restart(self):
        self.buffer.reset()  # Puffer löschen
        self.interrupt_locked = False  # IRQ Lock aufheben
        self.sm.active(1)  # SM wieder aktivieren!
    
    def activate(self, state=1):
        self.sm.active(state)

    def irq_handler(self, _):
        if self.interrupt_locked:
            return
     
        timeout = utime.ticks_ms() + 10  # 10 ms Timeout
     
        try:
            while not self.buffer.is_full():
                if (self.sm.rx_fifo() > 0) and (self.sm.active()):  # Prüft, ob noch Daten im FIFO sind
                    data = self.sm.get() ^ 0xFF
                    self.buffer.put(data)
                else:
                    # Falls kein neuer Interrupt (Hardwareausfall) kommt, nach 10 ms abbrechen
                    if utime.ticks_ms() > timeout:
                        break  # beende die Schleife

        except IndexError:
            pass
        
        if self.buffer.is_full():  # Puffer voll
            self.interrupt_locked = True  # IRQ verriegeln
            self.sm.active(0)  # State Machine Stop

    def get_data(self):
        return self.buffer.get_all()

    def reset_buffer(self):
        self.buffer.reset()


# --- SBUS-Decoder ---
class SBUSDecoder:
    """
    Extrahiert einen bestimmten SBUS-Kanal aus einem SBUS-Frame.
    :param frame: bytearray mit 25 Bytes (SBUS-Frame)
    :param channel: Kanalnummer (1-16), die extrahiert werden soll
    :return: Wert des angegebenen Kanals (0-2047)
    """
    @staticmethod
    def get_sbus_channel(frame, channel):
        if not (1 <= channel <= 16):
            return None
        
        channel -= 1
        
        channel_map = [
            (1, 2, 0, 11), (2, 3, 3, 11), (3, 4, 6, 11), (5, 6, 1, 11),
            (6, 7, 4, 11), (7, 8, 7, 11), (9, 10, 2, 11), (10, 11, 5, 11),
            (12, 13, 0, 11), (13, 14, 3, 11), (14, 15, 6, 11), (16, 17, 1, 11),
            (17, 18, 4, 11), (18, 19, 7, 11), (20, 21, 2, 11), (21, 22, 5, 11)
        ]
        
        b1, b2, shift, mask = channel_map[channel]
        return ((frame[b1] >> shift) | (frame[b2] << (8 - shift))) & 0x07FF
    
    @staticmethod
    def get_sbus_flags(frame, flag_type):
        """
        Extrahiert das Flag-Register aus einem SBUS-Frame und gibt den entsprechenden Status basierend auf flag_type zurück.
        :param frame: bytearray mit 25 Bytes, das den SBUS-Frame enthält
        :param flag_type: Integer (1-4) zur Auswahl des gewünschten Flags
        :return: Boolean-Wert des entsprechenden Flags
        """   
        flags = frame[23]
        flag_map = {
            1: (flags & 0x08) != 0,
            2: (flags & 0x04) != 0,
            3: (flags & 0x01) != 0,
            4: (flags & 0x02) != 0
        }
        return flag_map.get(flag_type, None)
    
    """
    Sucht im Datenpuffer nach einem gültigen SBUS-Frame und kopiert ihn den Puffer
    """
    @staticmethod
    def find_frame(data):
        for i in range(len(data) - 24):
            if data[i] == 0x0F and data[i + 24] == 0x00:
                return data[i:i+25]
        return None


# --- main ---
if __name__ == "__main__":
    def process_data():
        while True:
            if uart_receiver.buffer.is_full():  # Test auf vollen Enpfangspuffer
                data = uart_receiver.get_data()  # Daten aus Puffer holen
                #print([hex(d) for d in data])
                sbus_frame = SBUSDecoder.find_frame(data)  # vollständigen SBUS-Fram suchen
                
                if sbus_frame:  # wenn ein Frame erkannt, Kanal x ausgeben
                    channel = SBUSDecoder.get_sbus_channel(sbus_frame, 1)
                    print('Trust:', channel)
                    channel = SBUSDecoder.get_sbus_channel(sbus_frame, 2)
                    print('Rudder:', channel)
                    
                    flag = SBUSDecoder.get_sbus_flags(sbus_frame, 1)
                    print("Failsafe:", flag)
                    
                uart_receiver.restart()
            utime.sleep_ms(50)
    
    # Initialisierung der PIO
    BAUD = 100000  # SBUS-Baudrate 
    RX_PIN = 9  # Hardware-Pin des PR2024      
    uart_receiver = UART_RX(statemachine=0, rx_pin=RX_PIN, baud=BAUD)
    uart_receiver.activate(1)  # State Machine aktivieren
    
    try:
        process_data()  # Testfunktion
    except KeyboardInterrupt:
        print("Abbruch")
    
    uart_receiver.activate(0)  # Deaktivieren der PIO
    print("\ndone")
