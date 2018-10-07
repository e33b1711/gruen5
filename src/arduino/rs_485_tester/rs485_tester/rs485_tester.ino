
const char address='e';

void setup(){
  Serial.begin(9600);
}

void loop()
{
   
    String in_buffer;
    
    while(Serial.available()){
    char in_char;
    in_char = (byte)Serial.read();
    in_buffer += in_char;
    }
    
    //Serial.print(in_buffer);
    delay(200);
    
    if (in_buffer.charAt(0)==address){
    Serial.println(in_buffer);
    in_buffer="";
    }
    
    delay(200);

}





