import subprocess
import time
 
cmd_Conf = "gpio -g mode 18 out"
cmd_LED_ON = "gpio -g write 18 0"
cmd_LED_OFF = "gpio -g write 18 1"

subprocess.call(cmd_Conf.split())
subprocess.call(cmd_LED_ON.split())
time.sleep(5)
subprocess.call(cmd_LED_OFF.split())

