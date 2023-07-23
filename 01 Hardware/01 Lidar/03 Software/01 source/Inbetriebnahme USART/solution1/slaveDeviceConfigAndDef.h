/*
 * slaveDeviceConfig.h
 *
 * Created: 7/3/2023 10:04:33 PM
 *  Author: Thach
 */ 


#ifndef SLAVEDEVICECONFIG_H_
#define SLAVEDEVICECONFIG_H_

#define MAX_BYTE_SEND 31

#define RX_BUFFER_LEN 800
#define TX_BUFFER_LEN 100
#define NO_OF_RX_BUFFER 2
#define USART_TIME_PRO_BYTE_US 96

#define ACTIVE_USART_WATCHER 1

typedef struct{
	struct rxUnit{
		volatile uint8_t rxBuffer[NO_OF_RX_BUFFER][RX_BUFFER_LEN];
		volatile uint16_t toRxByte[NO_OF_RX_BUFFER];
		volatile uint16_t strReadPtr;
		const uint16_t rxLenMax;
		const uint8_t fifoLenMax;
		volatile uint8_t readFIFOPtr;
		volatile uint8_t writeFIFOPtr;
	}rxObj;
	struct txUnit{
		volatile uint8_t txBuffer[TX_BUFFER_LEN];
		volatile uint16_t toTxByte;
		volatile uint16_t strReadPtr;
		const uint16_t txLenMax;
		
	}txObj;
	struct status{
		volatile uint8_t uart:2;
		uint8_t initState:1;
		uint8_t crcActive:1;
		volatile uint8_t rxBufferState:2;//Leer, Belegt, Voll
		uint8_t nextPhase:1;
	}statusObj;
}slaveDevice_t;

typedef enum {
	ON,
	OFF
}state_t;

enum fifoState{
	EMPTY=0,
	FILLED,
	FULL
};

#endif /* SLAVEDEVICECONFIG_H_ */