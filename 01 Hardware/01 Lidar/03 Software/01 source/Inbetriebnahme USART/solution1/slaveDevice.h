/*
 * slave.h
 * F�r die Slave-Ger�t
 * Created: 21.06.2023 12:38:43
 * Author: Thach
 * Version: 0.1
 */ 


#ifndef SLAVE_H_
#define SLAVE_H_

#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <avr/interrupt.h>
#include <string.h>
#include "errorList.h"
#include "ATMegaXX09/USART/USART.h"
#include "timerUnit.h"
#include "slaveDeviceConfigAndDef.h"

extern processResult_t initDev(uint8_t USARTnumber, uint32_t baudrate, USART_CHSIZE_t bits, \
					USART_PMODE_t parity,USART_SBMODE_t stopbit, \
					bool sync, bool MPCM, uint8_t address, PORTMUX_USARTx_t PortMux);

extern processResult_t dataTx(uint8_t* data, uint16_t length);
extern processResult_t dataRx(uint8_t* data, uint16_t* length);

#endif /* SLAVE_H_ */