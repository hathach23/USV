/*
 * timerUnit.h
 *
 * Created: 6/29/2023 1:41:01 PM
 * Author: Thach
 */ 


#ifndef TIMERUNIT_H_
#define TIMERUNIT_H_

#include <avr/io.h>
#include <avr/interrupt.h>
#include "./ATMegaXX09/ATMegaXX09Clock.h"
#include "ATMegaXX09/USART/USART.h"
#include "Math/MinMax.h"
#include "error_list.h"
#include "slaveDeviceAPI.h"

#define NO_OF_SUBTIMER 2
#define NO_OF_USART 4

//erste Moeglichkeit
typedef struct  
{
	uint32_t value:31;
	uint8_t lock:1;
}tickGenerator;

//zweite Moeglichkeit
typedef struct{
	uint8_t day:5;
	uint8_t hour:5;
	uint8_t min:6;
	uint32_t us;
}clockTimer_t;

typedef struct{
	TCA_t *adr;
	uint8_t initStatus:1;
	uint8_t resolutionUs;
}timer_t;

typedef union{
	uint8_t value;
	struct{
		uint8_t ENABLE:1;//Bit 0, low bit
		uint8_t CLKSEL:3;
		uint8_t :1;
		uint8_t :1;
		uint8_t :1;//Bit 7, high bit
	}valueBitField;
}TCA0_CTRLA_t;

typedef union{
	uint8_t value;
	struct{
		uint8_t OVF:1;//Bit 0, low bit
		uint8_t :1;
		uint8_t :1;
		uint8_t :1;
		uint8_t CMP0:1;
		uint8_t CMP1:1;
		uint8_t CMP2:1;
		uint8_t :1;//Bit 7, high bit
	}valueBitField;
}TCA0_INTCTRL_t;

typedef union{
	uint8_t value;
	struct{
		uint8_t OVF:1;//Bit 0,1, low bit
		uint8_t :1;
		uint8_t :1;
		uint8_t :1;
		uint8_t CMP0:1;
		uint8_t CMP1:1;
		uint8_t CMP2:1;
		uint8_t :1;//Bit 7, high bit
	}valueBitField;
}TCA0_INTFLAGS_t;

typedef union{
	volatile uint16_t value;
	volatile struct{
		uint8_t lowByte:8;
		uint8_t highByte:8;
	}valueBitField;
}TCA0_CNT_t;

typedef union{
	volatile uint16_t value;
	volatile struct{
		uint8_t lowByte:8;
		uint8_t highByte:8;
	}valueBitField;
}TCA0_PER_t;

enum prescaler{
	DIV1 = 0x00,
	DIV2 = 0x01,
	DIV4 = 0x02,
	DIV8 = 0x03,
	DIV16 = 0x04,
	DIV64 = 0x05,
	DIV256 = 0x06,
	DIV1024 = 0x07
};

extern void timerInit(uint8_t resolutionUs, uint16_t prescaler);
extern void setUsartWatcherTimeout(uint8_t usartNr, uint32_t us);
extern uint32_t getUsartWatcherTimeout(uint8_t usartNr);
extern uint8_t waitUs(uint32_t us);
extern void waitCycle(uint32_t cycle);
extern uint8_t setWatchedObj(slaveDevice_t* input_p);

#endif /* TIMERUNIT_H_ */