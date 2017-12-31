dscrc_table = [
      0, 94,188,226, 97, 63,221,131,194,156,126, 32,163,253, 31, 65,
    157,195, 33,127,252,162, 64, 30, 95,  1,227,189, 62, 96,130,220,
     35,125,159,193, 66, 28,254,160,225,191, 93,  3,128,222, 60, 98,
    190,224,  2, 92,223,129, 99, 61,124, 34,192,158, 29, 67,161,255,
     70, 24,250,164, 39,121,155,197,132,218, 56,102,229,187, 89,  7,
    219,133,103, 57,186,228,  6, 88, 25, 71,165,251,120, 38,196,154,
    101, 59,217,135,  4, 90,184,230,167,249, 27, 69,198,152,122, 36,
    248,166, 68, 26,153,199, 37,123, 58,100,134,216, 91,  5,231,185,
    140,210, 48,110,237,179, 81, 15, 78, 16,242,172, 47,113,147,205,
     17, 79,173,243,112, 46,204,146,211,141,111, 49,178,236, 14, 80,
    175,241, 19, 77,206,144,114, 44,109, 51,209,143, 12, 82,176,238,
     50,108,142,208, 83, 13,239,177,240,174, 76, 18,145,207, 45,115,
    202,148,118, 40,171,245, 23, 73,  8, 86,180,234,105, 55,213,139,
     87,  9,235,181, 54,104,138,212,149,203, 41,119,244,170, 72, 22,
    233,183, 85, 11,136,214, 52,106, 43,117,151,201, 74, 20,246,168,
    116, 42,200,150, 21, 75,169,247,182,232, 10, 84,215,137,107, 53]

def dallas_crc8(data):
    crc = 0
    for d in data:
        offset = (crc ^ d) % 256
        crc = dscrc_table[offset]
    return crc

def send_setting(ser, setting):
    cmd = 'S'
    crc = dallas_crc8(setting)
    print "Sending:", cmd,"-",setting,"-",crc
    ser.write(cmd)
    for b in setting:
        ser.write(chr(b))
    ser.write(chr(crc))
    while True:
        line = ser.readline().rstrip().lstrip()
        print line
        if line== "<S":
            break
    time.sleep(2)


import serial, time, binascii
ser = serial.Serial('/dev/ttyACM0', 9600)

Red_LivingRoomFront = [0x01, 0x0, 0x0, 0x0, 0x0]
Blue_LivingRoomFront = [0x02, 0x0, 0x0, 0x0, 0x0]
Rad_LivingRoomFront = [0x0, 0x0, 0x0, 0x40, 0x0]

Red_LivingRoomBack = [0x04, 0x0, 0x0, 0x0, 0x0]
Blue_LivingRoomBack = [0x08, 0x0, 0x0, 0x0, 0x0]
Rad_LivingRoomBack = [0x0, 0x0, 0x0, 0x0, 0x80]

Red_Kitchen = [0x10, 0x0, 0x0, 0x0, 0x0]
Blue_Kitchen = [0x20, 0x0, 0x0, 0x0, 0x0]
Rad_Kitchen = [0x0, 0x0, 0x0, 0x0, 0x40]

#Red_WC = [0x40, 0x0, 0x0, 0x0, 0x0]
Blue_WC = [0x80, 0x0, 0x0, 0x0, 0x0]
Rad_WC = [0x0, 0x0, 0x0, 0x0, 0x10]

Red_Hall = [0x0, 0x1, 0x0, 0x0, 0x0]
Blue_Hall = [0x0, 0x2, 0x0, 0x0, 0x0]
Rad_Hall = [0x0, 0x0, 0x0, 0x0, 0x8]

Red_Study = [0x0, 0x0, 0x1, 0x0, 0x0]
Blue_Study = [0x0, 0x0, 0x2, 0x0, 0x0]
Rad_Study = [0x0, 0x0, 0x0, 0x0, 0x20]

Red_Guestbed = [0x0, 0x40, 0x0, 0x0, 0x0]
Blue_Guestbed = [0x0, 0x80, 0x0, 0x0, 0x0]
Rad_Guestbed = [0x0, 0x0, 0x0, 0x80, 0x0]

Red_Mainbed = [0x0, 0x20, 0x0, 0x0, 0x0]
Blue_Mainbed = [0x0, 0x10, 0x0, 0x0, 0x0]
Rad_Mainbed = [0x0, 0x0, 0x0, 0x0, 0x4]

Red_Smallbed = [0x0, 0x4, 0x0, 0x0, 0x0]
Blue_Smallbed = [0x0, 0x8, 0x0, 0x0, 0x0]
Rad_Smallbed = [0x0, 0x0, 0x0, 0x0, 0x2]

#Red_Bathroom = [0x0, 0x0, 0x0, 0x0, 0x0]
#Blue_Bathroom = [0x0, 0x0, 0x0, 0x0, 0x0]
Rad_Bathroom = [0x0, 0x0, 0x0, 0x20, 0x0]

Relay_A = [0x0, 0x0, 0x20, 0x0, 0x0]
Relay_B = [0x0, 0x0, 0x10, 0x0, 0x0]

Rads_Green = [0x0, 0x0, 0x0, 0x18, 0x0]
# missing greens - main bed, 

#>T
#Z0:2
#living room back - Z0D0:28.F1.BB.84.7.0.0.C9:16.75
#living room front - Z0D1:28.2F.3.83.7.0.0.E9:16.87
#Z1:2
#wc - Z1D0:28.D5.BE.84.7.0.0.71:17.12
#kitchen - Z1D1:28.77.A1.84.7.0.0.50:17.69
#Z2:1
#hall - Z2D0:28.7A.54.84.7.0.0.6E:18.12
#Z3:1
#small bed - Z3D0:28.86.A0.84.7.0.0.D8:16.56
#Z4:2
#main bed - Z4D0:28.40.1F.83.7.0.0.53:18.31
#guest bed - Z4D1:28.65.9B.84.7.0.0.5C:18.00
#Z5:1
#study - Z5D0:28.46.98.82.7.0.0.F4:16.50
#bathroom n/c - Z6:0
#<T



#setting = [0x0, 0x0,0x30,0x0,0x0]
#send_setting(ser, setting)

#print "Testing Red_LivingRoomFront..."
#send_setting(ser, Red_LivingRoomFront)
#raw_input("")
#
#print "Testing Blue_LivingRoomFront..."
#send_setting(ser, Blue_LivingRoomFront)
#raw_input("")
#
#print "Testing Rad_LivingRoomFront..."
#send_setting(ser, Rad_LivingRoomFront)
#raw_input("")
#
#print "Testing Red_LivingRoomBack..."
#send_setting(ser, Red_LivingRoomBack)
#raw_input("")
#
#print "Testing Blue_LivingRoomBack..."
#send_setting(ser, Blue_LivingRoomBack)
#raw_input("")
#
#print "Testing Rad_LivingRoomBack..."
#send_setting(ser, Rad_LivingRoomBack)
#raw_input("")
#
#print "Testing Red_Kitchen..."
#send_setting(ser, Red_Kitchen)
#raw_input("")
#
#print "Testing Blue_Kitchen..."
#send_setting(ser, Blue_Kitchen)
#raw_input("")
#
#print "Testing Rad_Kitchen..."
#send_setting(ser, Rad_Kitchen)
#raw_input("")
#
#print "Testing Red_WC..."
#send_setting(ser, Red_WC)
#raw_input("")
#
#print "Testing Blue_WC..."
#send_setting(ser, Blue_WC)
#raw_input("")
#
#print "Testing Rad_WC..."
#send_setting(ser, Rad_WC)
#raw_input("")
#
#print "Testing Red_Hall..."
#send_setting(ser, Red_Hall)
#raw_input("")
#
#print "Testing Blue_Hall..."
#send_setting(ser, Blue_Hall)
#raw_input("")
#
#print "Testing Rad_Hall..."
#send_setting(ser, Rad_Hall)
#raw_input("")
#
#print "Testing Red_Study..."
#send_setting(ser, Red_Study)
#raw_input("")
#
#print "Testing Blue_Study..."
#send_setting(ser, Blue_Study)
#raw_input("")
#
#print "Testing Rad_Study..."
#send_setting(ser, Rad_Study)
#raw_input("")
#
#print "Testing Red_Guestbed..."
#send_setting(ser, Red_Guestbed)
#raw_input("")
#
#print "Testing Blue_Guestbed..."
#send_setting(ser, Blue_Guestbed)
#raw_input("")
#
#print "Testing Rad_Guestbed..."
#send_setting(ser, Rad_Guestbed)
#raw_input("")
#
#print "Testing Red_Mainbed..."
#send_setting(ser, Red_Mainbed)
#raw_input("")
#
#print "Testing Blue_Mainbed..."
#send_setting(ser, Blue_Mainbed)
#raw_input("")
#
#print "Testing Rad_Mainbed..."
#send_setting(ser, Rad_Mainbed)
#raw_input("")
#
#print "Testing Red_Smallbed..."
#send_setting(ser, Red_Smallbed)
#raw_input("")
#
#print "Testing Blue_Smallbed..."
#send_setting(ser, Blue_Smallbed)
#raw_input("")
#
#print "Testing Rad_Smallbed..."
#send_setting(ser, Rad_Smallbed)
#raw_input("")
#
#print "Testing Rad_Bathroom..."
#send_setting(ser, Rad_Bathroom)
#raw_input("")
#
#print "Testing Relay_A..."
#send_setting(ser, Relay_A)
#raw_input("")
#
#print "Testing Relay_B..."
#send_setting(ser, Relay_B)
#raw_input("")
#
#print "Testing Rads_Green..."
#send_setting(ser, Rads_Green)
#raw_input("")




i=0
while True:
    if True:
        cmd = 'T'
        print "Sending:", cmd
        ser.write(cmd)
        while True:
            line = ser.readline().rstrip().lstrip()
            print line
            if line== "<T":
                break
#    setting = [0,0,0,0,0]
#    cmd = 'S'
#    crc = dallas_crc8(setting)
#    print "Sending:", cmd,"-",setting,"-",crc
#    ser.write(cmd)
#    for b in setting:
#        ser.write(chr(b))
#    ser.write(chr(crc))
#    while True:
#        line = ser.readline().rstrip().lstrip()
#        print line
#        if line== "<S":
#            break
#    time.sleep(2)
#    setting = [0xff,0xff,0xff,0xff,0xff]
#    cmd = 'S'
#    crc = dallas_crc8(setting)
#    print "Sending:", cmd,"-",setting,"-",crc
#    ser.write(cmd)
#    for b in setting:
#        ser.write(chr(b))
#    ser.write(chr(crc))
#    while True:
#        line = ser.readline().rstrip().lstrip()
#        print line
#        if line== "<S":
#            break
#    time.sleep(2)
#    # Too short sequence, should time out
#    setting = [0xff,0xff,0xff,0xff]
#    cmd = 'S'
#    crc = dallas_crc8(setting)
#    print "Sending:", cmd,"-",setting,"-",crc
#    ser.write(cmd)
#    for b in setting:
#        ser.write(chr(b))
#    ser.write(chr(crc))
#    while True:
#        line = ser.readline().rstrip().lstrip()
#        print line
#        if line== "<S":
#            break
#    time.sleep(2)
#    # Bad crc
#    setting = [0xff,0xff,0xff,0xff,0xff]
#    cmd = 'S'
#    crc = dallas_crc8(setting)
#    print "Sending:", cmd,"-",setting,"-",crc
#    crc += 1
#    ser.write(cmd)
#    for b in setting:
#        ser.write(chr(b))
#    ser.write(chr(crc))
#    while True:
#        line = ser.readline().rstrip().lstrip()
#        print line
#        if line== "<S":
#            break
    time.sleep(2)
