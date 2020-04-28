import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from Replay_Size import convert

beta = 5

MODELS = ["Vanilla", "Nature", "Double"]
Y = ["Average Score per 50 playouts", "Average Loss per 1000 updates"]
X = ["Number of Gameovers", "Number of Updates"]
TITLE = ["Performance of ", "Instability of "]
SCALE = [beta*10, 1000]
COLOR = ["g", "b", "r"]
LINE = ["-", "--"]

# load score data
SCORE = dict()
for model in MODELS:
    SCORE[model] = pd.read_csv(model+"DQN_score.csv").to_numpy().flatten()
    SCORE[model] = convert(SCORE[model], beta)
    SCORE[model] = [float(element) for element in SCORE[model]]

# load loss data
LOSS = dict()
for model in MODELS:
    LOSS[model] = pd.read_csv(model+"DQN_loss.csv").to_numpy().flatten()
    LOSS[model] = [float(element) for element in LOSS[model]]

# integrate and save dataset
DATA = [SCORE, LOSS]
with open("3DQN.json", "w") as file:
    file.write(json.dumps(DATA, indent=4))

# plotting
fig, axs = plt.subplots(2,3, figsize=(30,18))
fig.suptitle("Comparison: Three DQNs", fontsize=35)
for i in range(2):
    for j in range(3):
        y = DATA[i][MODELS[j]]
        axs[i,j]. plot([1+SCALE[i]*element for element in range(len(y))], y, COLOR[j]+LINE[i])
        axs[i,j].set_title(TITLE[i]+MODELS[j]+" DQN", fontsize=20, color=COLOR[j])
        axs[i,j].set_xlabel(X[i], fontsize=16)
        axs[i,j].set_ylabel(Y[i], fontsize=16)
plt.savefig("3DQN.eps")
plt.savefig("3DQN.png")
plt.show()

# zoom in the loss function of Nature DQN and Double DQN
fig, axs = plt.subplots(1,2, figsize=(20,10))
fig.suptitle("Convergence of Loss Function", fontsize=30)
axs[0].plot([1+1000*element for element in range(len(LOSS["Nature"]))], LOSS["Nature"], 'b--')
axs[0].set_title("Nature DQN", fontsize=20, color="blue")
axs[0].set_xlabel("Number of Updates", fontsize=16)
axs[0].set_ylabel("Average Loss per 1000 updates", fontsize=16)
axs[0].set_ylim(0, 0.08)
axs[1].plot([1+1000*element for element in range(len(LOSS["Double"]))], LOSS["Double"], 'r--')
axs[1].set_title("Double DQN", fontsize=20, color="red")
axs[1].set_xlabel("Number of Updates", fontsize=16)
axs[1].set_ylabel("Average Loss per 1000 updates", fontsize=16)
axs[1].set_ylim(0, 0.08)
plt.savefig("LossConvergence.eps")
plt.savefig("LossConvergence.png")
plt.show()