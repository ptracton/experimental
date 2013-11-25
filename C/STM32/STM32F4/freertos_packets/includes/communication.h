
#ifndef __COMMUNICATION_H__
#define __COMMUNICATION_H__

//
// OS level defines for creating tasks, queues, etc...
//
#define COMMUNICATION_STACK_SIZE 256
#define COMMUNICATION_QUEUE_SIZE 4

//
// List of packets or actions we know how to handle
//
#define COMMUNICATION_PACKET_PING     0xC0
#define COMMUNICATION_MAX_PACKET_TYPE 0xFF

//
// All of the different possible communication task errors
//
typedef enum
{
    ERROR_NONE = 0,
    ERROR_INDEX,
} xCommunication_Error_Type;
 

//
// Indicator if a message is part of reception or transmission
//
typedef enum{
    TRANSMIT_DATA =0,
    RECEIVE_DATA
} TX_OR_RX_Type;

//
// Structure and defines for our packet data types
//
#define COMMUNICATION_MAX_PACKET_SIZE 256   
typedef struct
{
    uint8_t type;    
    uint8_t size;
    uint8_t data[COMMUNICATION_MAX_PACKET_SIZE];    
    uint32_t crc;    
} xPacket_Type;

//
// The structure for a message passed in the queue
//
typedef struct 
{
    uint8_t rx_data;
    uint8_t error;
    TX_OR_RX_Type tx_or_rx;
    xPacket_Type packet;    
} xCommunication_Message;
   
//
// function pointer data type for packet handlers
//
typedef void (* vCommunicationFunctionPointer)( xPacket_Type *packet);

//
// our message passing Queue
//
extern xQueueHandle xCommunication_Queue;

//
// Public API
//
void vCommunication_Task(void *pvParameters);
void vPacket_Init(xPacket_Type *packet);


#endif
