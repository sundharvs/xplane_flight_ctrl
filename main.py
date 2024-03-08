from time import sleep
import xpc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd, csd
import json
# from scipy import optimize
# import control

data_dict = {}
duration = 90
t = np.linspace(0,duration,int(duration/0.01 + 1))
phase = 2 * np.pi * (0.05 * t + (2 - 0.05) / (2 * duration) * t**2)
chirp = 0.05*np.sin(phase)

def chirp_exec():
    el_chirp_response = []

    with xpc.XPlaneConnect() as client:
    #     data = client.getDREFs()
    #     print(data)
        for i in range(len(t)):
            client.sendCTRL([chirp[i], -998, -998, -998, -998, -998])
            try:
                el_chirp_response += client.getDREF("sim/flightmodel/position/Q")
            except:
                pass
            sleep(0.01)

    with open('./el_chirp.json', 'w+') as file:
        data_dict = {"time": t.tolist(), "response": el_chirp_response}
        json.dump(data_dict,file)


with open('./el_chirp.json', 'r') as file:
    try:
        data_dict = json.load(file)
    except json.decoder.JSONDecodeError:
        chirp_exec()
    
t = data_dict["time"]
el_chirp_response = data_dict["response"]

# def model(el):
#     sys = control.tf([],[])
#     # y = control.forced_response(sys,t,chirp)
#     return y
    
# optimize.curve_fit(model,chirp,el_chirp_response)

# tf = csd(chirp.tolist(), el_chirp_response)[0] / psd(chirp.tolist())[0]

# print(tf)

plt.figure(1)
plt.plot(t,el_chirp_response)
plt.show()