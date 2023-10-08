/*
 * lidarComProtocol.h
 *
 * Created: 10/8/2023 3:13:45 PM
 *  Author: Thach
 */ 


#ifndef LIDARCOMPROTOCOL_H_
#define LIDARCOMPROTOCOL_H_

#define STX_SYMBOL 0x02
#define LIDAR_DEFAULT_ADDR 0x00
#define ETX_SYMBOL 0x03

//siehe "Telegramme zur Konfiguration und Bedienung der Lasermesssysteme LMS2xx-V2.30"-S36-37 f�r mehrere Informationen
enum lidarCommando{
	INIT_AND_RESET = 0x10,
	OP_MODE_SEL = 0x20,
	MEASURED_DATA_REQ = 0x30,
	STATUS_REQ = 0x031,//Nur f�r LMS2xx m�glich
	ERROR_OR_TEST_TELEGRAM_REQ = 0x32,
	OP_DATA_COUNTER_REQ = 0x35,
	AVG_MEASURED_DATA_REQ = 0x36,
	SEG_MEASURED_DATA_REQ = 0x37,
	LIDAR_TYPE_REQ = 0x3A,
	MEASURED_CONFIG_CHANGE = 0x3B,
	MEASURED_DATA_WITH_FIELD_DATA_REQ = 0x3E,
	SEG_AVG_MEASURED_DATA_REQ = 0x3F,
	FIELD_ABC_CONFIG = 0x40,
	ACTIVE_FIELD_SET_CHANGE = 0x41,
	PWD_CHANGE = 0x42,
	SEG_MEASURED_DATA_AND_REFLECTANCE_REQ = 0x44,
	FIELD_REQ = 0x45,
	LEARNING_MODE_START = 0x46,
	FIELDS_STATUS_OUT_REQ = 0x4A,
	BAUDRATE_OR_LIDAR_TYPE_DEF = 0x66,
	ANGLE_RNG_POSITIONING_SUP = 0x69,
	LIDAR_CONFIG_P1_REQ = 0x74,//Nur f�r LMS2xx m�glich
	MEASURED_DATA_WITH_REFLECTANCE_REQ = 0x75,
	MEASURED_DATA_IN_XY_COORD_REQ = 0x76,
	LIDAR_CONFIG_P1 = 0x77,//Nur f�r LMS2xx m�glich
	LIDAR_CONFIG_P2_REQ = 0x7B,//Nur f�r LMS2xx m�glich
	LIDAR_CONFIG_P2 = 0x7C//Nur f�r LMS2xx m�glich
};


#endif /* LIDARCOMPROTOCOL_H_ */