import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

beta = 5

Exp2 = dict()
replay_size = ["250K", "500K", "750K", "1000K"]
for size in replay_size:
    Exp2[size] = pd.read_csv("score_Exp2_"+size+".csv").to_numpy().flatten()
	
# compute the average per beta data points
def convert(Array, beta):
    k = 0
    y = list()
    while beta*k < len(Array):
	lst = list()
	m = 0
	while m < beta:
	    if beta*k+m >= len(Array):
		break
	    lst.append(Array[beta*k+m])
	    m += 1
	y.append(np.mean(lst))
	k += 1
		
min_L = 999999999
max_score = 0
for size in replay_size:
    Exp2[size] = convert(Exp2[size], beta)
    min_L = min(min_L, len(Exp2[size]))
    max_score = max(max_score, max(Exp2[size]))
json.dump(Exp2, open("NatureDQN_Exp2.json", "w"))
	
# plotting
fig, axs = plt.subplots(2,2, figsize=(20,20))
fig.suptitle("Scores of Breakout ($\epsilon$: 1 to 0.05)", fontsize = 35, color="limegreen")
for i in range(2):
    for j in range(2):
	y = Exp2[replay_size[2*i+j]]
	axs[i,j].plot([beta*10*t for t in range(len(y))], y, "limegreen")
	axs[i,j].set_title("Replay Size = "+replay_size[2*i+j], fontsize = 23)
	axs[i,j].set_xlabel("Number of Gameovers", fontsize = 20)
	axs[i,j].set_ylabel("Average Score per "+str(int(beta*10))+ " playouts", fontsize = 20)
	axs[i,j].set_xlim(0, beta*10*min_L)
	axs[i,j].set_ylim(0, max_score)
plt.savefig("Replay_Size_Exp2.eps")
plt.savefig("Replay_Size_Exp2.png")
plt.show()
