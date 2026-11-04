import serial

ser = serial.Serial('COM10', 115200, timeout=1, rtscts=False, dsrdtr=False)

while True:
    if ser.in_waiting > 0:
        byte = ser.read(1)
        print(f"Received byte: {int.from_bytes(byte, 'little')}")