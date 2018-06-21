## 使用微信＋树莓派＋Arduino＋服务器构建智能家庭小助手

<img src="./image/bannerImage.png" width = "100%" height = "100%" align=center />

### 前言
这是我去年的大创项目《一种基于微信的主动式家庭智能监测系统设计与实现》，因为时间关系，一直都没有好好的梳理一遍应该如何去复现它，最近时间较为充裕，我会较为仔细的描述清楚该项目的核心难点（其实并没有难点🙄）。当初报这个项目是为了学习一些硬件的简单相关知识，再结合一下前年（17年的项目要在16年年末申报）的社会热点问题，当时大家都比较热衷于“智能家庭”的概念。当时的小米“家庭智能”套件火的是一塌糊涂，甚至还出了贺岁版礼包（如果我没记错的话），再结合当时对自己的技术路线的一个定位，需要弥补一些关于硬件的知识，遂有了这个项目。

因为时间间隔的比较久远，不保证复现过程中100%正确，如果你有跟着走，出现了问题请务必告知，我们一起完善！大部分都是`Python`和`Arduino`代码，建表SQL因为没法保证大家的物料跟我是一致的，而且大家也不一定会做的跟我完全一样，这块就保留了吧。当然，如果你喜欢论文严谨的格式，也可以到知网down下与[本项目相关的渣作](http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST2018&filename=BJGY201802014&uid=WEEvREcwSlJHSldRa1FhdkJkVWI3b1ZpYW5qRm5Fekw3WWhmM1JGaW4xaz0=$AiWoHpiIFem7UrzGXWMU2pCrz7uWVXrw-rnFauXDWKZCB8nomqJ3KA!!&v=MTY3NDBKeWZNZDdHNEg5bk1yWTlFWUlSOGVYMUx1eFlTN0RoMVQzcVRyV00xRnJDVVJMS2ZZZVJ1RnlIbVY3dkI=)

### 物料准备

我将使用微信公众号、树莓派、Arduino和一台乞丐版配置的云服务器构建一个智能家庭小助手，用于协助我们对室内环境有一个较好的把控。如果你什么都没有可以参考以下清单先行购买物料（所有的必须物料下来，勉强三百多一些？）：

**1. 一块树莓派。**版本随意，如果你资金比较充裕，可以购买最新型号的树莓派，毕竟最新的3B型号wifi模块信号更好，整体的处理速度更快。￥150~300
**2. 一套Arduino开发套件。**注意，是开发套件而不是Arduino这一块板子，我们需要开发套件中的其它元器件。￥150~300
**3. 一台云服务器。**如果你要用自己的电脑也可以，在校园网、小区、公司内记得先做内网穿透，不过一台乞丐版的服务器也没多少钱，能省很多事。￥0~10
**4.微信公众号。**如果你之前没申请过的话，貌似开通审核得等两三天？￥0

### 信息配置

如果一切顺利，现在你的手上应该有一块树莓派、一套Arduino开发套件、一台云服务器、一个微信公众号。微信提供了一套公众号开发SDK，可以使用它，虽然官方提供开发文档已经非常成熟了，但还是觉得不够简洁。在此推荐大家使用[itchatmp](https://github.com/littlecodersh/itchatmp)。

  **微信公众号**：
  进入[微信公众平台](https://mp.weixin.qq.com/)在左下角找到“开发”-“基本配置”，
  
  <img src="https://i.loli.net/2018/06/21/5b2b6df2228fc.png" width = "40%" height = "40%" align=center />
  
  在该页面中填写相关信息，
  
  <img src="https://i.loli.net/2018/06/21/5b2b6e2816c70.png" width = "80%" height = "80%" align=center />
  
  **服务器地址（URL）：**填写IP地址。但必须是公网IP或者已经做了内网穿透的IP地址，也可解析好域名后填入对应域名。
  **令牌（Token）：**用于微信公众号和服务器进行双向交互时的验证。
  **消息加解密密钥：**随意。
  所有内容都填写完毕后，别着急提交。进行下一步，

### 服务器
  登录服务器后，先检查是否安装了Python环境（可直接上Python3）。安装完成后，使用pip下载itchatmp，

  ```shell
  $ pip install itchatmp
  ```
  下载完成后，新建一个.py文件（此处以mp.py为例），在文件中写下，
  ```python
  import itchatmp

  itchatmp.update_config(itchatmp.WechatConfig(
    # 填写上一步在微信公众号的配置内容
     token='yourToken',
     appId = 'yourAppId',
     appSecret = 'yourAppSecret'))
     
  @itchatmp.msg_register(itchatmp.content.TEXT)
     def text_reply(msg):
       return msg['Content']

  itchatmp.run()
  ```
  此时执行，（需要root权限）
  ```shell
  $ python mp.py
  ```
  看到下边这句话后就可以去微信公众号点击确认啦~
  ```shell
  itchatmp started! press Ctrl+C to exit.
  ```
  
  **效果：**
    进入到对应的微信公众号中，你输入任何内容，它都会给你返回相同的内容。如果微信公众平台告诉你Token验证失效估计就是你的IP地址不对。

### 数据库
使用数据库是为了存储数据（完全可以使用txt文件来维护），在此为了简化手拼SQL易出错以及本项目并不需要进行多少性能优化的情况下，直接采用[ORM（对象关系映射技术）](https://www.cnblogs.com/wgbs25673578/p/5140482.html)。
  P.S.我将采用`sqlalchemy`这个框架进行，在[廖雪峰的博客](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014320114981139589ac5f02944601ae22834e9c521415000)上有较为细致的讲解，大家可以先自行研究一番到底是个什么东西。

  这是定义好的硬件类，其实也就是硬件表，
  ```python
  # 硬件表
  class Hardware(Base):
     __tablename__ = 'hardware'

     id = Column(Integer, primary_key=True)
     name = Column(String(64), nullable=False)
     status = Column(Integer, nullable=False)
     num = Column(Integer, nullable=False)
  ```
  新建一个py文件（以test.py为例），在其中写下，
  ```python
  from sqlalchemy import create_engine
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy import Column, String, Integer
  from sqlalchemy.orm import sessionmaker

  # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
  engine = create_engine('mysql+mysqldb://root:mimamima@localhost:3306/restful?charset=utf8')
  Base = declarative_base()
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind = engine)
  session = Session()
  ```
  到这一步为止，就完成了使用ORM进行MySQL数据库操作的铺垫。接下来，我们将进行数据库的增删改查方法的编写。
  1. 增加一个元器件：
  ```python
  # 添加电子原件方法
  # 原件name及针脚num需要配置
  # 原件状态默认关闭
  def addNewUnit(hardwareName, status, num):
       Base.metadata.create_all(engine)
       Session = sessionmaker(bind=engine)
       session = Session()
       unit = Hardware(
           name = hardwareName, 
           status = status,
           num = num)
       session.add(unit)
       session.commit()
  ```
  2. 修改一个元器件的状态：
  ```python
  # 执行write操作
  def writeHardware(hardwarename, status, num):
       unit = readHardware(hardwarename)
       unit = session.query(Hardware).get(unit.id)
       if unit:
           unit.status = status
           if 'Unit' in hardwarename:
               unit.num = num;
           session.add(unit)
           session.commit()
           return '操作成功'
       return '操作失败，请联系管理员'
  ```
  3. 读取一个元器件的状态：
  ```python
  # 执行read操作
  def readHardware(hardwarename):
       Base.metadata.create_all(engine)
       Session = sessionmaker(bind = engine)
       session = Session()
       unit = session.query(Hardware).filter_by(name=hardwarename).first()
       return unit
  ```
  4. 稍微做了点封装的update方法：
  ```python
  #  电子原件执行read或write筛选方法
  def updateStatusWithHardware(tableName, operatorStatus, hardwarename, status):
       if tableName == 'hardware':
           if operatorStatus == 1:
               return writeHardware(hardwarename, status, 0)
           else:
               return readHardware(hardwarename)
  ```
  现在我们完成了test.py的编写，主要完成了使用ORM技术编写了操作数据库的各种方法。接下来，我们要使用微信公众号对数据库进行修改。

### 上位机配置
在这个环节中，我们要做到用户发送“开灯”、“关灯”、“开风扇”、“温度”等消息给公众号后，能够在数据库中看到状态被修改并且反馈。

简单的来概括一下要做的工作：首先要让服务器接收到公众号发送而来的消息；其次要对发送者进行筛选，不能谁都可以操作这套系统；接着匹配消息，执行不同的方法；最后给公众号反馈回消息。

服务器接收公众号发送的消息我们已经在第一步中完成了，现在要对接收到的消息体进行解析，根据userID来筛选谁能对这套系统进行操作。我的做法非常简单，用一个"pjhubs.txt"文件保存了能够操作这套系统的用户ID。每次接收到消息时，都先从消息体中取出fromUserName字段数据与txt文件中的数据进行比对，如果在txt文件中才允许接着进行操作。
```python
import itchatmp
import test

# 配置微信公众号信息
itchatmp.update_config(itchatmp.WechatConfig(
    token='你的token',
    appId = '你的appId',
    appSecret = '你的appSecret'))

# 接收用户消息
@itchatmp.msg_register(itchatmp.content.TEXT)
def text_reply(msg):
    toUserName = msg['FromUserName']
    content = msg['Content']
    isContain = 0
    # pjhubs.txt为有权限的用户列表
    f = open("pjhubs.txt","r")
    lines = f.readlines()
    for line in lines:
        if line[:-1] == toUserName:
            isContain = 1;   
    if isContain == 0:
        return '该系统并未对您开放，请联系PJ进行配置'
    else:
        if content == '添加':
            # test.addNewUnit('tempUnit', 1, 2)
            return '操作成功!'
        elif content == '开灯':
            return test.updateStatusWithHardware('hardware', 1, 'redLED', 1)
        elif content == '关灯':
            return test.updateStatusWithHardware('hardware', 1, 'redLED', 0)
        elif content == '温度':
            unit = test.updateStatusWithHardware('hardware', 0, 'tempUnit', 1)
            returnString = '当前温度为：' + str(unit.num) + '°'
            return returnString
        elif content == '开风扇':
            return test.updateStatusWithHardware('hardware', 1, 'tempUnit', 1)
        elif content == '关风扇':
            return test.updateStatusWithHardware('hardware', 1, 'tempUnit', 0)
        
# 新用户关注公众号时
@itchatmp.msg_register(itchatmp.content.EVENT)
def user_management(event):
    if(event['Event']=='subscribe'):
        return u'欢迎来到PJHubs，如果你想试用室内环境智能监测系统，请联系PJ'
itchatmp.run()
```
执行，
```shell
$ python mp.py
```
在微信公众号中发送“开灯”、“关灯”、“开风扇”、“温度”等指令都会对数据库进行操作。此时可以select对应表查看数据是否一致再进行下一步。

### API编写
这是知乎上一些[关于API的内容讲解](https://www.zhihu.com/question/38594466)。我们在此使用[Flask](http://docs.jinkan.org/docs/flask/)轻量级的web框架进行API编写。主要是给树莓派操作数据库使用的。
    通过pip安装好flask后，我们可以先尝试写一个最简单的restful格式的API：
```python
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request
from flask import abort
from flask import make_response
import test

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return 'Get out!🙂'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
```
此时我们去浏览器中输入ip地址或域名，即可看到“Get out!🙂”这句话。现在我们要接着编写几个资源访问路径以便树莓派访问。
```python
# 获取所有硬件信息（求快可以这么写）
@app.route('/dachuang/api/v1/allHardware')
def get_allHardware():
    LED = test.readHardware('redLED')
    UNIT= test.readHardware('tempUnit')
    LEDres = { 'id' : LED.id,
            'name' : LED.name,
            'status' : LED.status,
            'num' : LED.num }
    UNITres = { 'id' : UNIT.id,
                'name' : UNIT.name,
                'status' : UNIT.status,
                'num' : UNIT.num }
    return jsonify([LEDres, UNITres])

# 更新固定元器件（求快用了GET，最好是POST）
@app.route('/dachuang/api/v1/updateHardware', methods=['GET'])
def get_updateHardware():
    hardwarename = request.args.get('hardwarename')
    status = request.args.get('status')
    num = request.args.get('num')
    if status == '3':
        unit = test.readHardware(hardwarename)
        test.writeHardware(hardwarename, unit.status, num)
    else:
        test.writeHardware(hardwarename, unit.status, num)
    return jsonify({'code' : '1'})
```
我们只需要起两个API服务即可满足要求。此时我们可以根据写好的API访问规则到浏览器中验证一番。

### 下位机配置——树莓派
树莓派是整套系统的灵魂所在，对上承载着数据库的更新，对下负担着Arduino的操作。当然，如果不考虑性能你可以直接用Arduino的wifi模组，直接对API发起请求。
    
树莓派首先要去在固定时间间隔内轮询特定API，根据API反馈回来的数据对固定串口发送特定字符，接收Arduino传递上来的数据，拼接API更新数据库。
    
serial是对树莓派上的串口进行操作库，urllib2是网络请求库，json是解析和发送JSON格式库。
```python
import serial
import urllib2
import json

hostname = 'http://你的地址/dachuang/api/v1/allHardware'
# /dev/ttyACM0 是树莓派上编号为0的USB口（可以在/dev目录下通过观察拔插对应的USB口找到对应的编号）
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 4)

while 1:
    r = urllib2.Request(hostname)
    r = urllib2.urlopen(r)
    res = r.read()
    result = json.loads(res)
    print result
    send = ''
    # 通过json库解析完后的数据就是字典
    if result[0]['status'] == 1:
        send += 'a'
    else:
        send += 'A'
    if result[1]['status'] == 1:
    send += 'b'
    else:
    send += 'B'
    # 从下位机Arduino上读取到的数据拼接URL发送回服务器，更新数据库
    ser.write(send)
    response = ser.readall()
    if '' != response:
        response = response[0:2]
        ret = urllib2.Request("http://你的地址/dachuang/api/v1/updateHardware?hardwarename=tempUnit&status=3" + '&num=' + response)
        ret = urllib2.urlopen(ret)
```
我在此重新定义了一套操作流程，
a -> “开灯”
A -> “关灯”
b -> “开风扇”
B -> “关风扇”
因为受到Arduino本身性能的影响，如果你还给它发一长串的字符串比如“open light”等，那估计单单就解析并匹配，分时操作已经过了。😂。因此我才想重新定义一套ASCII码关系映射，并且限制树莓派每次轮询的时间为4秒一次，可根据用户所搭建的下位机硬件系统复杂适度增减轮询时间。

### 下位机配置——Arduino
Arduino要做的事情只有接收串口数据，解析串口数据，根据数据分别操作不同的硬件。Arduino用C写的，定义了一套规则，用起来非常顺手亲切。
```c
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
  //读取A0口的电压值，温度传感器所在串口
  int n = analogRead(A0);    
  //使用浮点数存储温度数据，温度数据由电>压值换算得到
  float vol = n * (5.0 / 1023.0*100);   
  if ( Serial.available() ) {
      // 向串口写入温度
      Serial.println(vol);
      // 读取树莓派写入串口的数据
      int res = Serial.read();
      // 根据ASCII码执行不同硬件操作函数
      if (res == 97) {
        digitalWrite(yellowLED, HIGH);
      }
      if (res == 65){
        digitalWrite(yellowLED, LOW);
      }
      if (res == 98) {
        digitalWrite(fanPin, HIGH);
      }
      if (res == 66) {
        digitalWrite(fanPin, LOW);
      }
    }
    // 超过30°后开启高温预警，蜂鸣器奏响和风扇打开
    if (vol > 30) {    
        buzzerBegin();
    }
}

// 蜂鸣器响铃
void buzzerBegin() {
  digitalWrite(fanPin, HIGH);
  digitalWrite(REDled, HIGH);
  //频率从200HZ 增加到800HZ，模拟警报声
  for(int i=200;i<=800;i++) {
    tone(Buzzer,i);
    delay(5);
  }
  delay(100);
  for(int i=800;i>=200;i--) {
    tone(Buzzer,i);
    delay(5);
  }

  digitalWrite(REDled, LOW);
  digitalWrite(fanPin, LOW);
}
```

### 上下位机联调
至此我们完成了全部的基础工作，在联调的过程中，当初我也发生了非常多的问题，这无法避免，稍不注意电路连错了以后就全盘皆输了，在此我只能祝大家好运，Arduino连接各个元器件的方式并没有展开，因为我相信大家的电路设计一定比我强！👍

在联调的过程中，你需要做的是，
1. 运行restful.py，把整套API服务跑起来；
2. 运行mp.py，让公众号和服务器打通;
3. Arduino通过USB与树莓派相连后，树莓派再通电；
4. 在公众号上发送指令，观察Arduino上元器件状态变化。

**结果：**

  <img src="./image/image1.gif" width = "50%" height = "50%" align=center />
  
  <img src="./image/image2.gif" width = "50%" height = "50%" align=center />
  

