import matplotlib.pyplot as plt
import pandas as pd
from numpy import mean

# import raw data
x = pd.read_csv("TEST_score.csv").to_numpy().flatten()

print("Test Nature DQN by", 10*len(x), "playouts.")

# plt histogram of average scores
plt.figure(figsize=(12,12))
plt.hist(x, bins=20, color="deepskyblue")
plt.title("The Distribution of Test Scores", fontsize=20)
plt.xlabel("Average Score per 10 playouts", fontsize=16)
plt.ylabel("Counts", fontsize=16)
plt.savefig("Histogram_TestScores.eps")
plt.savefig("Histogram_TestScores.png")
plt.show()

# count the number of average socres within interval [a,b]
def f_count(x, a, b):
    count = 0
    for score in x:
        if score>= a and score<= b:
            count += 1
    return(count)
    
# compute credible interval
def cred_I(x, alpha, digits):
    step = 0.01*(max(x)-min(x))
    lower = mean(x)
    upper = mean(x)
    while True:
        k = f_count(x, lower, upper)
        if k/len(x)>=alpha:
            break
        lower -= step
        upper += step
    lower = round(lower, digits)
    upper = round(upper, digits)
    return((lower,upper))
    
# print out the mean and the credible interval of average scores
print("The 95% credible interval:",cred_I(x,0.95, digits=2))
print("The mean of average scors:", round(mean(x),2))
