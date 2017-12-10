#define yellowLED 13


void setup()  {
  Serial.begin(9600); // 9600 bps
  pinMode(yellowLED, OUTPUT);
}
void loop() {
 if ( Serial.available()) {
      if('y' == Serial.read()) {
         operatorLED(13, 1);
     } else {
         operatorLED(13, 0); 
     }
  }
}


void operatorLED(int hardwarenum, int hardwarestatus) {
    if(hardwarenum == 13) {
        if(hardwarestatus == 1) {
            digitalWrite(yellowLED, HIGH);
            Serial.println("yellowLED HIGH");
          } else {
            digitalWrite(yellowLED, LOW);  
            Serial.println("yellowLED LOW");
          }
      }
}
