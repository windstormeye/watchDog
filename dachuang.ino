#define yellowLED 13
#define REDled 12
#define Buzzer 8
#define fanPin 2

void setup()  {
  Serial.begin(9600); // 9600 bps
  pinMode(yellowLED, OUTPUT);
  pinMode(Buzzer,OUTPUT);
  pinMode(REDled,OUTPUT);
  pinMode(fanPin,OUTPUT);
}
void loop() {
  if ( Serial.available() ) {
      int res = Serial.read();
      if (res == 97) {
        Serial.println(res);
        operatorLED(13, 1);   
      } 
      if (res == 65){
        Serial.println(res);
        operatorLED(13, 0);   
      }
      if (res == 98) {
        Serial.println(res);
        digitalWrite(fanPin, HIGH);
      } 
      if (res == 66){
        Serial.println(res);
        digitalWrite(fanPin, LOW);  
      }
//      if('y' == Serial.read()) {
//           operatorLED(13, 1);
//      } 
//      if('Y' == Serial.read()) {
//           operatorLED(13, 0); 
//      }
//      if('r' == Serial.read()) {
//           Serial.println(vol);
//      }
    }
//  int n = analogRead(A0);    //读取A0口的电压值
//  float vol = n * (5.0 / 1023.0*100);   //使用浮点数存储温度数据，温度数据由电压值换算得到
//  Serial.println(vol);
//  delay(1000);        
//  if (vol > 27) {    // 温度
//      buzzerBegin();
//  } 
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

void buzzerBegin() {
  digitalWrite(fanPin, HIGH);
  digitalWrite(REDled, HIGH);
  for(int i=200;i<=800;i++)                    //用循环的方式将频率从200HZ 增加到800HZ
  {
    tone(Buzzer,i);                            
    delay(5);                              
  }
  delay(1000);
  //最高频率下维持1秒钟
  for(int i=800;i>=200;i--)
  {
    tone(Buzzer,i);
    delay(5);                              
  }
  
  noTone(Buzzer);
  digitalWrite(REDled, LOW);
  digitalWrite(fanPin, LOW);
}

