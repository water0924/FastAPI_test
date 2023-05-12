import time
import main

main.more()
print("Loading",end="")
for i in range(20):
    print(".",end="",flush=True)
    time.sleep(0.5)