# ESP-Vihag

parts list (/flower pot): <br/>
1* IRFZ44n N-Channel Fet; <br/>
2* BC547b NPN transistors (or similar, pinouts may differ!) <br/>
3* 1KΩ resistors <br/>
1* 1n4007 diode (or similar, MUST BE Shottky) <br/>
1* 3 pin male jumper with 2 pin jumper cap <br/>
1* 4 pin female header <br/>
2* 6 pin female header

## Configuration
MUST CHANGE:<br />
MQTT_CLIENT_ID give it a random name that (I recommend use for topics, more lower)<br />
MQTT_GTOPIC for simplicity use the same as MQTT_CLIENT_ID, but put a g in or at the end<br />
MQTT_STOPIC same for MQTT_GTOPIC but with an s<br />
NETWORK_SSID Name of your Wi-Fi network<br />
NETWORK_PASSWORD Password of your Wi-Fi network, leave it blank if there is None<br />
<br />

OTHER (OPTIONAL):<br />
MQTT_BROKER default: broker.mqttdashboard.com, works perfectly, but you can use any kind<br />
MQTT_USER not required, optional<br />
MQTT_PASSWORD not required, optional<br />
MQTT_UPDATE default: 420 (4 minutes), time (seconds) between mqtt publishes<br />
MEASURE_INTERVAL default: 420 (4 minutes), time (seconds) between getting a sample<br />
MEASURE_SAMPLE_AM default: 10<br />
PUMP_PIN default: 2 (pin 2)<br />
SOIL_PIN default: 39 (pin 3)<br />
TANK_PIN default: 34 (pin 4)<br />
OVERFLOW_PIN default: 35 (pin 5)<br />
PUMP_TRIGGER default: 120 (not recommended)<br />
PUMP_TIME default: 8, pump active cycle time (seconds)<br />
PUMP_SLEEP default: 8, time between active pump cycles (seconds)<br />
CALIBRATION_MODE default: True (recommendend on startup)<br />
