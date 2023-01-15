#esp_pot_v1.2
from umqtt.simple import MQTTClient
from machine import ADC, Pin, Timer
from ujson import dumps
from time import sleep
import network

class script:
    def __init__(self):
        #NETWORKING CONFIG
        self.MQTT_CLIENT_ID = "espdev_8yp0db"
        self.MQTT_BROKER = "broker.mqttdashboard.com"
        self.MQTT_USER = ""
        self.MQTT_PASSWORD = ""
        self.MQTT_GTOPIC = "espdev_8gp0db"
        self.MQTT_STOPIC = "espdev_8sp0db"
        self.MQTT_UPDATE = 3600
        self.NETWORK_SSID = "
        self.NETWORK_PASSWORD = ""
        #OTHER CONFIG
        self.PUMP_PIN = 2
        self.SOIL_PIN = 39 #VP
        self.TANK_PIN = 34
        self.OVERFLOW_PIN = 35
        self.MEASURE_INTERVAL = 3600
        self.MEASURE_SAMPLE_AM = 10
        self.PUMP_TRIGGER = 180
        self.PUMP_TIME = 2
        self.PUMP_SLEEP = 2
        self.CALIBRATION_MODE = True
        #NETWORK SETUP
        self.wconnect()
        #MQTT SETUP
        self.client = MQTTClient(self.MQTT_CLIENT_ID, self.MQTT_BROKER, user=self.MQTT_USER, password=self.MQTT_PASSWORD)
        self.client.connect()
        self.client.publish(self.MQTT_STOPIC,dumps("Connected"))
        #OTHER
        self.pump = Pin(self.PUMP_PIN, Pin.OUT)
        self.soil_sen = ADC(Pin(self.SOIL_PIN, Pin.IN))
        self.tank_sen = Pin(self.TANK_PIN, Pin.IN)
        self.overflow_sen = Pin(self.OVERFLOW_PIN, Pin.IN)
        self.overflow_sen.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)
        self.pump_state = False
        self.mqtt_timer = Timer(0)
        self.soil_timer = Timer(1)
        self.pump_timer = Timer(2)
        self.mqtt_timer.init(period=self.MQTT_UPDATE*1000, callback=lambda t: self.mqtt_upt())
        self.soil_timer.init(period=self.MEASURE_INTERVAL*1000, callback=lambda t: self.get_sample())
        self.sample_set = []
        self.sample = 0.
    
    def wconnect(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(False)
        self.sta_if.active(True)
        self.sta_if.connect(self.NETWORK_SSID, self.NETWORK_PASSWORD)
        while not self.sta_if.isconnected():
            sleep(0.1)
            print(".",end="")
    
    def get_sample(self):
        self.sample_set.append(self.soil_sen.read())
        if len(self.sample_set) > self.MEASURE_SAMPLE_AM:
            self.sample_set.pop(0)
        self.sample = sum(self.sample_set)/len(self.sample_set)

    def mqtt_upt(self):
        if not self.sta_if.isconnected():
            self.wconnect()
        self.client.connect()
            
        if self.CALIBRATION_MODE:
            self.client.publish(self.MQTT_STOPIC, dumps("Calibration enabled."))
        elif not self.tank_sen.value():
            self.client.publish(self.MQTT_STOPIC, dumps("Water tank running low."))
        elif self.sample > self.PUMP_TRIGGER:
            self.client.publish(self.MQTT_STOPIC, dumps("Watering..."))
        else:
            self.client.publish(self.MQTT_STOPIC, dumps("Operational"))
        self.client.publish(self.MQTT_GTOPIC,dumps(self.sample))
        self.client.disconnect()
    def set_pump(self):
        self.pump.value(True)
        self.pump_state = True
        main.pump_timer.init(period=main.PUMP_TIME*1000,mode=Timer.ONE_SHOT,callback= lambda t: self.reset_pump())

    def reset_pump(self):
        self.pump.value(False)
        self.pump_state = False
        sleep(self.PUMP_SLEEP)
    
    def callback(self, pin):
        self.pump_timer.deinit()
        try:
            self.client.publish(self.MQTT_STOPIC, dumps(""))
        except:
            self.client.connect()
        self.client.publish(self.MQTT_STOPIC, dumps("OVERFLOW ALERT!"))
        self.pump.value(False)
        self.pump_state = False

main = script()
    
while True:
    if main.pump.value() == 1 and main.sample < main.soil.read():
        main.pump.value(0)
    if main.CALIBRATION_MODE or not main.tank_sen.value():
        main.pump.value(False)
    else:
        if main.sample > main.PUMP_TRIGGER and main.overflow_sen.value():
            if not main.pump_state:
                main.set_pump()
