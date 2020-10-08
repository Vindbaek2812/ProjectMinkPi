can="0000" + "3400" + "93020074"

print("0x" + can[4:6])
data1 = "0x" + can[4:5]
data2 = "0x" + can[5:6]
value2 = int(data1, 0) + 256 * int(data2,0)
print(value2)