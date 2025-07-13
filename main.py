import serial
import serial.tools.list_ports
import time

byte_dict = {
    "MODE": "00000001",
    "IN": "00000010",
    "OUT": "00000011",
    "GPIO": "00000100",
    "LOW": "00000101",
    "HIGH": "00000110",
    "SERVO1": "00000111",
    "SERVO1W": "00001000"
}

def choose_port():
    ports = serial.tools.list_ports.comports()
    port_names = []
    for port in ports:
        print(port.name)
        port_names.append(port.name)
    chosen = input("Choose the port for the Arduino: ")
    if chosen in port_names:
        return chosen
    elif "COM" + chosen in port_names:
        return "COM" + chosen
    else:
        return choose_port()

def choose_arduino_type():
    types = ["UNO"]
    print(f"Supported types: {types}")
    chosen = input("Arduino type: ")
    if chosen in types:
        return chosen
    else:
        return choose_arduino_type()

def int_to_bin(val:int):
    if val > 255:
        raise ValueError("Value must be <=255")
    
    coefficients = [128, 64, 32, 16, 8, 4, 2, 1]
    output = [0, 0, 0, 0, 0, 0, 0, 0]
    for coefficient in coefficients:
        if coefficient <= val:
            val -= coefficient
            output[coefficients.index(coefficient)] = 1
    output_string = ""
    for bit in output:
        output_string += str(bit)
    return output_string

def write(text:str):
    arduino.write((text + '\n').encode('utf-8'))

def read():
    data = arduino.readline().decode().strip()
    return data

def write_read(write_text:str):
    write(write_text)
    time.sleep(0.05)
    output = read()
    return output

def write_bytes(num_bytes: int, byte_list: list[str]):
    if len(byte_list) != num_bytes:
        raise ValueError(f"Expected {num_bytes} bytes, but got {len(byte_list)}.")
    
    byte_array = bytearray()
    for b in byte_list:
        if len(b) != 8 or not all(c in '01' for c in b):
            raise ValueError(f"Invalid byte: '{b}'. Each must be an 8-character binary string.")
        byte_array.append(int(b, 2))

    arduino.write(byte_array)

def read_and_print_chunks():
    data = arduino.readline().decode().strip()
    chunks = [data[i:i+8] for i in range(0, len(data), 8)]
    for chunk in chunks:
        print(chunk)
    return chunks

if __name__ == "__main__":
    PORT = choose_port()
    TYPE = choose_arduino_type()
    arduino = serial.Serial(port=PORT, baudrate=115200, timeout=1)
    time.sleep(2)
    while True:
        command_raw = input()
        command = command_raw.split()
        if command[0] == "MODE":
            try:
                pin = int(command[1])
                if pin >= 0 and pin <= 13:
                    mode = command[2]
                    if mode == "IN" or mode == "OUT":
                        if len(command) == 3:
                            byte_list = []
                            for v in command:
                                if v in byte_dict:
                                    byte_list.append(byte_dict[v])
                                else:
                                    byte_list.append(int_to_bin(int(v)))
                            print(byte_list)
                            write_bytes(num_bytes=len(byte_list), byte_list=byte_list)
                            time.sleep(0.05)
                            # print(read())
                        else:
                            print("INVALID COMMAND - Too Many Arguments")
                    else:
                        print("INVALID COMMAND - Invalid Mode")
                else:
                    print("INVALID COMMAND - Invalid Pin")
            except Exception as e:
                print(f"INVALID COMMAND - Error - {e}")
        elif command[0] == "GPIO":
            try:
                pin = int(command[1])
                if pin >= 0 and pin <= 13:
                    state = command[2]
                    if state == "LOW" or state == "HIGH":
                        if len(command) == 3:
                            byte_list = []
                            for v in command:
                                if v in byte_dict:
                                    byte_list.append(byte_dict[v])
                                else:
                                    byte_list.append(int_to_bin(int(v)))
                            print(byte_list)
                            write_bytes(num_bytes=len(byte_list), byte_list=byte_list)
                            time.sleep(0.05)
                        else:
                            print("INVALID COMMAND - Too Many Arguments")
                    else:
                        print("INVALID COMMAND - Invalid State")
                else:
                    print("INVALID COMMAND - Invalid Pin")
            except Exception as e:
                print(f"INVALID COMMAND - Error - {e}")
        elif command[0] == "SERVO1":
            try:
                pin = int(command[1])
                if pin >= 0 and pin <= 13:
                    if len(command) == 2:
                        byte_list = []
                        for v in command:
                            if v in byte_dict:
                                byte_list.append(byte_dict[v])
                            else:
                                byte_list.append(int_to_bin(int(v)))
                        print(byte_list)
                        write_bytes(num_bytes=len(byte_list), byte_list=byte_list)
                        time.sleep(0.05)
                    else:
                        print("INVALID COMMAND - Too Many Arguments")
                else:
                    print("INVALID COMMAND - Invalid Pin")
            except Exception as e:
                print(f"INVALID COMMAND - Error - {e}")
        elif command[0] == "SERVO1W":
            try:
                pwm_val = int(command[1])
                if pwm_val >= 0 and pwm_val <= 255:
                    if len(command) == 2:
                        byte_list = []
                        for v in command:
                            if v in byte_dict:
                                byte_list.append(byte_dict[v])
                            else:
                                byte_list.append(int_to_bin(int(v)))
                        print(byte_list)
                        write_bytes(num_bytes=len(byte_list), byte_list=byte_list)
                        time.sleep(0.05)
                    else:
                        print("INVALID COMMAND - Too Many Arguments")
                else:
                    print("INVALID COMMAND - PWM Value out of Range")
            except Exception as e:
                print(f"INVALID COMMAND - Error - {e}")
        else:
            print("INVALID COMMAND - No Such Command")