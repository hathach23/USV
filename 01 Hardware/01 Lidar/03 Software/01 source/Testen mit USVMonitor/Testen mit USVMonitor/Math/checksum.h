/*
 * checksum.h
 *
 * Created: 7/7/2023 9:12:38 AM
 * Author: Thach
 */ 


#ifndef CHECKSUM_H_
#define CHECKSUM_H_

#include <stdint.h>

extern uint8_t crc8(uint8_t* data, uint16_t len, uint8_t polynom);
extern uint16_t crc16(uint8_t* data, uint16_t len, uint16_t polynom);

#endif /* CHECKSUM_H_ */