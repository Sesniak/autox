import network
import espnow
import machine
import struct

# Inicjalizacja Wi-Fi
net = network.WLAN(network.STA_IF)
net.active(True)

#Inicjalizacja ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

#Konfiguracja pinow
pwm_l = machine.PWM(machine.Pin(placeholder), freq=5000)
dir1 = machine.Pin(placeholder, machine.Pin.OUT)
dir2 = machine.Pin(placeholder, machine.Pin.OUT)

pwm_r = machine.PWM(machine.Pin(placeholder), freq=5000)
dir3 = machine.Pin(placeholder, machine.Pin.OUT)
dir4 = machine.Pin(placeholder, machine.Pin.OUT)

def map_value(val, in_min, in_max, out_min, out_max):
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def set_motor(speed, pin_a, pin_b, pwm_pin):
    #Funkcja kierunku i predkosci
    if speed > 0:
        pin_a.value(1)
        pin_b.value(0)
        duty = int((speed / 255) * 1023) #Przeliczenie -255/255 na MicroPythona (0-1023)
        pwm_pin.duty(duty)
    elif speed < 0:
        pin_a.value(0)
        pin_b.value(1)
        duty = int((abs(speed) / 255) * 1023)
        pwm_pin.duty(duty)
    else:
        pin_a.value(0)
        pin_b.value(0)
        pwm_pin.duty(0)

while True:
    #Oczekiwanie na dane (100ms)
    host, msg = esp.recv(100)
    
    if msg:
        #Rozpakowanie danych
        x, y = struct.unpack('ii', msg)
        
        #Konwersja ADC na zakres sterowania
        forward_backward = map_value(y, 0, 4095, -255, 255) #Przod / Tyl
        left_right= map_value(x, 0, 4095, -255, 255) #Lewo / Prawo
        
        #Ignorowanie mikrodrgan
        if abs(forward_backward) < 25: forward_backward = 0
        if abs(left_right) < 25: left_right = 0
        
        #Skrecanie
        speed_l = forward_backward + left_right
        speed_r = forward_backward - left_right
        
        # Ograniczenie do zakresu
        speed_l = max(-255, min(255, speed_l))
        speed_r = max(-255, min(255, speed_r))
        
        #Ustawienie predkosci na silnikach
        set_motor(speed_l, dir1, dir2, pwm_l)
        set_motor(speed_r, dir3, dir4, pwm_r)
    else:
        #Jesli nadajnik nie przesyla informacji, zetrzymuje silniki
        set_motor(0, dir1, dir2, pwm_l)
        set_motor(0, dir3, dir4, pwm_r)