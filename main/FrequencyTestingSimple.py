import time

errorIndex=21
delay=10
count=0
value="4-6-10"
#0|1|10|11|14|15|17|21
if(errorIndex==0 or errorIndex==1 or errorIndex==10 or errorIndex==11 or errorIndex==14 or errorIndex==15 or errorIndex==17 or errorIndex==21):
    print("We have a match")
else:
    print("nothing was matched")

def svdmk():
    while True:
        time.sleep(1)
        count = count + 1
        if (count << 10):
            print(count)
        if (count == delay):
            print(count)
            count = 0


