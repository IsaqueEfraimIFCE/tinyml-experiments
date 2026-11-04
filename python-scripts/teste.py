import serial
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import cifar10

# Load CIFAR-10 test data
(_, _), (testX, testY) = cifar10.load_data()
testX = testX.astype(np.uint8)
SERIAL_PORT = 'COM9'
BAUD_RATE = 115200
DELAY = 1  
accuracy = 0


try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud...")
        
        for idx, image in enumerate(testX):
            image=image.flatten()
            image_bytes = image.tobytes()
            print(image_bytes)
            ser.write(image_bytes)
            print(f"Image {idx} sent to ESP32.")
            time.sleep(DELAY)
            result = ser.read(1) 
            if result:
                predicted = result[0]
                actual = int(testY[idx][0])
                if predicted == actual:
                    igual += 1

                print(f"Predicted: {predicted}, Actual: {actual}, Match: {predicted == actual}")
            else:
                print("No response received.")

    print(f"\nFinished. Accuracy: {igual}/{len(testX)} = {igual/len(testX)*100:.2f}%")

except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nStopped by user.")