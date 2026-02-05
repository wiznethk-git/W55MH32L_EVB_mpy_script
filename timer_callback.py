from machine import Timer
import time
#Initialze TIM4，freq: 1Hz
tim = Timer(11, freq=1)
tim.callback(lambda t: print("Timer tick"))
print("source_freq = ", tim.source_freq())
print("tim.freq = ", tim.freq())
print("tim.period = ", tim.period())
