#coding:utf-8
import time
import RPi.GPIO as GPIO
import threading

print("Raspberrari")

GPIO.setmode(GPIO.BCM)

#Motor variablen initialisieren
ENA = 13		#L298 Aktivieren A
ENB = 20		#L298 Aktivieren B

IN1 = 19		#Motor 1
IN2 = 16		#Motor 2
IN3 = 21		#Motor 3
IN4 = 26		#Motor 4

#Ultraschall variablen initialisieren
ECHO = 4		#Empfänger  
TRIG = 17		#Übertragung

#Pin Initialisierung
GPIO.setwarnings(False)

#Motor auf LOW Initialisieren
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(100)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(100)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

#Motorsteuerung
##Vorwärts
def car_forward():
	print "Vorwärts"
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)

##Rückwärts
def car_rewards():
	print "Rückwärts"
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)

##Links
def car_left():
	print "Links"
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)

##Rechts
def car_right():
	print "Rechts"
	GPIO.output(ENA, True)
	GPIO.output(ENB, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)

##Stop
def engine_stop():
	print "Engine Stop"
	GPIO.output(ENA, False)
	GPIO.output(ENB, False)
	GPIO.output(IN1, False)
	GPIO.output(IN2, False)
	GPIO.output(IN3, False)
	GPIO.output(IN4, False)

#Geschwindigkeit
##Vorderachse
def ena_speed(EA_num):
	speed = hex(eval("0x" + EA_num))
	speed = int (speed, 5)
	print "Speed %d" %speed
	ENA_pwm.ChangeDutyCycle(speed)

##Hinterachse
def enb_speed(EB_num):
	speed = hex(eval("0x" + EB_num))
	speed = int (speed, 5)
	print "Speed %d" %speed
	ENB_pwm.ChangeDutyCycle(speed)


#Ultraschall Abstandsmessung
##Rückgabewer in Zentimetern
def get_distance():
	time.sleep(0.1)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	time.sleep(0.1)
	return (t2 - t1) * 340 / 2 * 100

#Ultraschall Abstandsanzeige
##Rückgabewer in Zentimetern
##Anzeige auf Konsole
def show_distance():
	dis_send = int(Get_Distence())

	if dis_send < 255:
		print "Distance: %d cm" %dis_send
		tcpCliSock.send("\xFF")
		time.sleep(0.005)
		tcpCliSock.send("\x03")
		time.sleep(0.005)
		tcpCliSock.send("\x00")
		time.sleep(0.005)
		tcpCliSock.send(chr(dis_send))
		time.sleep(0.005)
		tcpCliSock.send("\xFF")
		time.sleep(0.1)

#######TESTING#######
i = 0;
while i < 2:
	eingabe = raw_input("Fahrtrichtung: ")
	print "Eingabe " + eingabe
	if (eingabe == "forward"):
		car_forward()
		i = 1
		time.sleep(3)
		exit(0)
	elif (eingabe == "reward"):
		car_rewards()
		i = 1
		time.sleep(3)
		exit(0)
	elif (eingabe == "right"):
		car_right()
		i = 1
		time.sleep(3)
		exit(0)
	elif (eingabe == "left"):
		car_left()
		i = 1
		time.sleep(3)
		exit(0)
	elif (eingabe == "stop"):
		engine_stop()
		i = 2
		time.sleep(3)
		exit(0)
	else:
		print("Fehlerhafte Eingabe")
