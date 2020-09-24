import re
alarms=''
def compacted():
    alarmvalue = 'c000c0'
    errorIndex = 0
    index = 0
    errorList=''
    errors = [80, 40, 20, 10, 8, 4, 2, 1]
    #alarmvalue = str(bytearray(data).hex())
    col1 = alarmvalue[0:2]
    col2 = alarmvalue[2:4]
    col3 = alarmvalue[4:6]
    columns = [col1, col2, col3]
    print(col1, col2, col3)
    for value in columns:
        index=index+1
        if (re.search('[a-zA-Z]', value)):
            if (col3=="c0"):
                errorList=errorList + '16-17-'
        else:
            value = int(value)
            for error in errors:
                if (error <= value):
                    value = value - error
                    # print(errorIndex)
                    errorList = (errorList + str(errorIndex) + '-')
                errorIndex = errorIndex + 1

    global alarms
    alarms = errorList.rstrip('-')
    print('"' + alarms + '"')


def firstTestToMakeItWork():
    x = 1
    y = 2
    z = 4
    a = 8
    b = 10
    c = 20
    d = 40
    e = 80
    alarmvalue = "331081"
    col1 = alarmvalue[0:2]
    col2 = alarmvalue[2:4]
    col3 = alarmvalue[4:6]
    columns = [col1, col2, col3]
    print(col1, col2, col3)
    for value in columns:
        # print(value)
        value = int(value)
        value = value - e
        if (not isinstance(value, int)) or value >= 0:
            print(e)
        else:
            value = value + e
        value = value - d
        if (not isinstance(value, int)) or value >= 0:
            print(d + value)
        else:
            value = value + d
        value = value - c
        if (not isinstance(value, int)) or value >= 0:
            print(c)
        else:
            value = value + c
        value = value - b
        if (not isinstance(value, int)) or value >= 0:
            print(b)
        else:
            value = value + c
        value = value - b
        if (not isinstance(value, int)) or value >= 0:
            print(b)
        else:
            value = value + b
        value = value - a
        if (not isinstance(value, int)) or value >= 0:
            print(a)
        else:
            value = value + a
        value = value - z
        if (not isinstance(value, int)) or value >= 0:
            print(z)
        else:
            value = value + z
        value = value - y
        if (not isinstance(value, int)) or value >= 0:
            print(y)
        else:
            value = value + y
        value = value - x
        if (not isinstance(value, int)) or value >= 0:
            print(x)
        else:
            value = value + x
        print("============")

compacted()