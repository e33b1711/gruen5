//token ring frame:  enthält nur ganze !w!LI_OG_L1!3$ kommandos, andet mit <nxt_address>&



#include <SoftwareSerial.h>

SoftwareSerial com(10,11);    
String com_in_buffer="";       
String rs485_in_buffer=""; 
String rs485_out_buffer="";    




void setup()  
{
  com_in_buffer.reserve(40);
  rs485_in_buffer.reserve(40);
  rs485_out_buffer.reserve(40);

  Serial.begin(9600);
//  Serial.print("gateway ");
//  Serial.write(address);
//  Serial.println(" gestartet.");
//
  com.begin(9600);
//  com.print("gateway ");
//  com.write(address);
//  com.println(" gestartet.");

}

void loop(){
  char in_char;
  int index;
  boolean listening=true;

  //listening on com and rs485
  while(listening){
    in_char='a';
    if(com.available()){
      in_char = (byte)com.read();
      com_in_buffer += in_char;
      if (in_char=='$'){
        rs485_out_buffer += com_in_buffer;
        com_in_buffer="";
      }
    }
    if(Serial.available()){
      in_char = (byte)Serial.read();
      rs485_in_buffer += in_char;
      if (in_char=='&'){
        listening=false;
      }
    }
  }

  //sending on com and rs485
  index=rs485_in_buffer.length();
  //bin ich mit senden dran? ja, falls frame beendet und nxt_address == address
  if ((rs485_in_buffer.charAt(index-2)==address) && (rs485_in_buffer.charAt(index-1)=='&')){
    delay(10);
    Serial.print(rs485_out_buffer);
    Serial.write(nxt_address);
    Serial.write("&");
    rs485_out_buffer="";
  }
  //senden auf com
  if (index>2){
  com.print(rs485_in_buffer.substring(0,index-2));
  }
  rs485_in_buffer="";

}

