import network
import espnow
import machine
import struct
import time

#Inicjalizacja Wi-Fi
net = network.WLAN(network.STA_IF)
net.active(True)

#Inicjalizacja ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

#Trzeba wpisac MAC odbiornika w autku
peer = 'placeholder'
esp.add_peer(peer)

#Konfiguracja pinow
adc_x = machine.ADC(machine.Pin(placeholder))
adc_y = machine.ADC(machine.Pin(placeholder))

#Ustawienie zakresu napiecia
adc_x.atten(machine.ADC.ATTN_11DB)
adc_y.atten(machine.ADC.ATTN_11DB)

while True:
    #Odczyt pozycji joysticka
    x = adc_x.read()
    y = adc_y.read()
    
    #Zapakowanie danych
    data = struct.pack('ii', x, y)
    
    #Wyslanie danych
    try:
        esp.send(peer, data)
    except OSError:
        pass
        
    time.sleep(0.02)  #Wysylanie danych co 20ms