//TO DO: andere serielle Schnittstelle benutzen, asccii codierte integer übertragen, für menschen lesbar


void init_comm()
{
  // initialize rs485
  Serial1.begin(9600);
  // reserve 200 bytes for the inputString and outputString
  inputString.reserve(50);

  //standard message format für frei text missbrauchen
  send_message("info", ("Gestartet. unit name: " + unit_name), 0 );


}

void send_message(String out_messageType, String out_address, int out_value){
  String message='!' + out_messageType + '!' + out_address + '!' + String(out_value, DEC) + "$";
  Serial1.print(message);
}

void handle_comm(){
  hear();
}



void hear(){
  // handle COM commands
  while (Serial1.available() && !(messageComplete)) {

    // get the new byte:
    char inChar = (char)Serial1.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '$') {
      messageComplete = true;
    } 
  }
  int i;
  while (messageComplete) {

    //message parser
    int index1=inputString.indexOf('!');
    int index2=inputString.indexOf('!', index1+1);
    int index3=inputString.indexOf('!', index2+1);
    int index4=inputString.indexOf('$');

    String in_messageType=inputString.substring(index1+1, index2);


    String addressString=inputString.substring(index2+1,index3);

    String valueString=inputString.substring(index3+1,index4);
    int in_value=valueString.toInt();

    //debbuging
    if (in_messageType!="t"){
      Serial.println("parsing message:");
      Serial.println(in_messageType);
      Serial.println(addressString);
      Serial.println(in_value);
    }
    //debbuging

    //message handler

    if (in_messageType=="post_all" && addressString==unit_name){
      post_all(); 
    }

    if (in_messageType=="r") {
      if (is_my_state(addressString)){
        send_message("i", addressString, address_to_value(addressString));
      }
    }

    if (in_messageType=="w") {   
      write_state_silent(addressString, in_value);
    }

    //wieder auf Empfang gehen
    inputString="";
    messageComplete= false;
  }
}

void post_all(){
  Serial1.print("!info!" + unit_name + "!posting all: start!0$");
  int i;
  for (i=0; i<num_d_states; i++){
    Serial1.print("!w!" + d_address[i] + "!" + value_d[i] + "!0$");
  }

  for (i=0; i<num_l_states; i++){
    Serial1.print("!w!" + l_address[i] + "!" + value_l[i] + "!0$");
  }

  for (i=0; i<num_r_states; i++){
    Serial1.print("!w!" + r_address[i] + "!" + value_r[i] + "!0$");
  }

  for (i=0; i<num_t_states; i++){
    Serial1.print("!w!" + t_address[i] + "!" + value_t[i] + "!0$");
    Serial1.print("!w!" + h_address[i] + "!" + value_h[i] + "!0$");
  }

  for (i=0; i<num_u_states; i++){
    send_message("w", u_address[i], value_u[i]);
  }

  send_message("info", unit_name + " posting all: end", 0);
}




