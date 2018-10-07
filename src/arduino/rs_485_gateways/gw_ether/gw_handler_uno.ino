#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network.
// gateway and subnet are optional:
byte mac[] = { 
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192,168,178, 200);
IPAddress gateway(192,168,178, 1);
IPAddress subnet(255, 255, 255, 0);


// telnet defaults to port 23
EthernetServer server(23);
boolean alreadyConnected = false; // whether or not the client was connected previously


String com_out_buffer="";    
String com_in_buffer="";       
String rs485_in_buffer=""; 
String rs485_out_buffer=""; 

long timer;




void setup()  
{

  com_in_buffer.reserve(40);
  rs485_in_buffer.reserve(40);
  rs485_out_buffer.reserve(40);

  Serial.begin(9600);




  Ethernet.begin(mac, ip, gateway, subnet);
  // start listening for clients
  server.begin();

  // Serial.print("Setup ended.");
  
  timer=millis();

}

//token ring frame:  enthält nur ganze !w!LI_OG_L1!3$ kommandos, andet mit <nxt_address>&



void loop(){
  char in_char;
  int index;
  boolean listening=true;



  //listening on inserver and rs485
  while(listening){
    in_char='a';


    EthernetClient client = server.available();

    if (client) {
      if (!alreadyConnected) {
        // clead out the input buffer:
        client.flush();    
        //        Serial.println("We have a new client");
        //        client.println("Hello, client!"); 
        alreadyConnected = true;
      }
    }

    if (alreadyConnected) {
      if(client.available() > 0){
        in_char = (byte)client.read();
        com_in_buffer += in_char;
        if (in_char=='$'){
          rs485_out_buffer += com_in_buffer;
          com_in_buffer="";
        }
      }
    }
    if(Serial.available()){
      in_char = (byte)Serial.read();
      rs485_in_buffer += in_char;
      if (in_char=='&'){
        listening=false;
      }
    }
    
    //check for token ring timeout
    if (timer+5000<millis()){
      Serial.print(nxt_address);
      Serial.print('&');
      timer=millis();
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
    timer=millis();
    rs485_out_buffer="";
  }
  //senden auf com
  if (index>2){


    server.println(rs485_in_buffer.substring(0,index-2));

  }
  rs485_in_buffer="";

}




