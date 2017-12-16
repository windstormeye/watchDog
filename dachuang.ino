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
  int n = analogRead(A0);    //读取A0口的电压值
  float vol = n * (5.0 / 1023.0*100);   //使用浮点数存储温度数据，温度数据由电压值换算得到
  if ( Serial.available() ) {
      Serial.println(vol);  
      int res = Serial.read();
      if (res == 97) {
        digitalWrite(yellowLED, HIGH);
      } 
      if (res == 65){
        digitalWrite(yellowLED, LOW);
      }
      if (res == 98) {
        digitalWrite(fanPin, HIGH);
      } 
      if (res == 66){
        digitalWrite(fanPin, LOW);  
      }
    }
          
    if (vol > 30) {    // 温度
        buzzerBegin();
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
  delay(100);
  for(int i=800;i>=200;i--)
  {
    tone(Buzzer,i);
    delay(5);                              
  }
  
  noTone(Buzzer);
  digitalWrite(REDled, LOW);
  digitalWrite(fanPin, LOW);
}

