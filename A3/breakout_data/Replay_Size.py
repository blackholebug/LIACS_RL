import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

beta = 5

replay_size = ["250K", "500K", "750K", "1000K"]
COLOR = ["mediumspringgreen", "limegreen", "mediumseagreen", "forestgreen"]
SCALE = [beta*10, 1000]
LINE = ["-", "--"]
TITLE = ["Performance: ", "Instability: "]
X = ["Number of Gameovers", "Number of Updates"]
Y = ["Average Score per 50 playouts", "Average Loss per 1000 updates"]

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
	return(y)
  
# load and organize score data
SCORE = dict()
min_L = 999999999
max_score = 0
for size in replay_size:
	SCORE[size] = pd.read_csv("score_Exp2_"+size+".csv").to_numpy().flatten()
    SCORE[size] = convert(SCORE[size], beta)
    SCORE[size] = [float(element) for element in SCORE[size]]
    min_L = min(min_L, len(SCORE[size]))
	max_score = max(max_score, max(SCORE[size]))
	

# integrate and save data
LIMITS = {"x":[min_L, min_l], "y":[max_score, max_loss]}
Exp2 = [SCORE, LOSS]
json.dump(Exp2, open("NatureDQN_Exp2.json", "w"))
	
# plotting
fig, axs = plt.subplots(2,4, figsize=(40,20))
fig.suptitle("Experience Replay ($\epsilon$: 1 to 0.05)", fontsize = 35)
for i in range(2):
	for j in range(4):
		y = Exp2[i][replay_size[j]]
		axs[i,j].plot([1+SCALE[i]*t for t in range(len(y))], y, color=COLOR[j], linestyle=LINE[i])
		axs[i,j].set_title(TITLE[i]+"Buffer Size = "+replay_size[j], fontsize = 23, color=COLOR[j])
		axs[i,j].set_xlabel(X[i], fontsize = 20)
		axs[i,j].set_ylabel(Y[i], fontsize = 20)
		axs[i,j].set_xlim(0, SCALE[i]*LIMITS["x"][i])
		axs[i,j].set_ylim(0, LIMITS["y"][i])
plt.savefig("Replay_Exp2.eps")
plt.savefig("Replay_Exp2.png")
plt.show()

# zoom in the case when buffer size = 500K
fig, axs = plt.subplots(1,2, figsize=(20,10))
fig.suptitle("Replay Buffer Size: 500K", fontsize=30, color="limegreen")
axs[0].plot([beta*10*ele for ele in range(len(SCORE["500K"]))], SCORE["500K"], color="limegreen", linestyle="-")
axs[0].set_title("Performance", fontsize=20)
axs[0].set_xlabel(X[0], fontsize=16)
axs[0].set_ylabel(Y[0], fontsize=16)
axs[1].plot([1000*ele for ele in range(len(LOSS["500K"]))], LOSS["500K"], color="limegreen", linestyle="--")
axs[1].set_title("Instability", fontsize=20)
axs[1].set_xlabel(X[1], fontsize=16)
axs[1].set_ylabel(Y[1], fontsize=16)
plt.savefig('Replay_500K.eps')
plt.savefig("Replay_500K.png")
plt.show()