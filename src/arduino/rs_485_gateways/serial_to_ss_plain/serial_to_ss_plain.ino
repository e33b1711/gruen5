  //token ring frame:  enthält nur ganze !w!LI_OG_L1!3$ kommandos, andet mit <nxt_address>&
  
  
  
  #include <SoftwareSerial.h>
  
  SoftwareSerial com(10, 11); 
  
  
  
  
  void setup()  
  {
    
    Serial.begin(9600);

    com.begin(9600);
    
    Serial.println("Serial to SoftwareSerial transparent started.");
    
  }
  
  
  void loop(){
    while(Serial.available()){
      com.write((byte)Serial.read());
    }
    
     while(com.available()){
      Serial.write((byte)com.read());
    }
    
    
    }

  


