message50="32000000"
message150="96000000"
message2000="d0070000"
message4000="a00f0000"
message25005="ad610000"
message1000025="b9860100"
messageMAX="ffffffff"

onMes=message2000

byte1=onMes[0:2]
byte2=onMes[2:4]
byte3=onMes[4:6]
byte4=onMes[6:8]

print(int("0x" + byte4+byte3+byte2+byte1,0))
