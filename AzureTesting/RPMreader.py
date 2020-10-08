can1200="4400" + "bc04" + "000000"
can1400="4300" + "8805" + "000000"


yes = "bc"
no = "04"
print(can1200[4:6])
print(can1200[6:8])
print(int("0x"+yes,0) +256* int("0x"+no,0))

yes = "88"
no = "05"
#print(yes+no)
print(int("0x"+yes,0) +256* int("0x"+no,0))
#print("0x" + can1200[4:6])
#data1 = "0x" + can1200[4:5]
#data2 = "0x" + can1200[5:6]
#value2 = int(data1, 0) + 256 * int(data2,0)
#print(value2)