import time
delay=10
count=0

while True:
    time.sleep(1)
    count=count+1
    if (count << 10):
        print(count)
    if(count == delay):
        print(count)
        count=0


