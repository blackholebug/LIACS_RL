import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from Replay_Size import convert

beta = 5

# the performance of Vanilla DQN
Vanilla = pd.read_csv("VanillaDQN.csv").to_numpy().flatten()
Vanilla = convert(Vanilla, beta)
plt.figure(figsize=(10,10))
plt.plot([beta*10*t for t in range(len(Vanilla))], Vanilla)
plt.title("The Performance of Vanilla DQN", fontsize=20, color="blue")
plt.xlabel("Number of Gameovers", fontsize=16)
plt.ylabel("Average Score per "+str(int(10*beta))+" playouts", fontsize=16)
plt.ylim(0,10)
plt.savefig("VanillaDQN.eps")
plt.savefig("VanillaDQN.png")
plt.show()

# the performance of Nature DQN
Nature = pd.read_csv("score_Exp2_1000K.csv").to_numpy().flatten()
Nature = convert(Nature, beta)
plt.figure(figsize=(10,10))
plt.plot([beta*10*t for t in range(len(Nature))], Nature, "g")
plt.title("The Performance of Nature DQN", fontsize=20, color="green")
plt.xlabel("Number of Gameovers", fontsize=16)
plt.ylabel("Average Score per "+str(int(10*beta))+" playouts", fontsize=16)
plt.ylim(0,10)
plt.savefig("NatureDQN.eps")
plt.savefig("NatureDQN.png")
plt.show()

# the performance of Double DQN
Double = pd.read_csv().to_numpy().flatten()
Double = convert(Double, beta)