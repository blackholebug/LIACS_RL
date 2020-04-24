import numpy as np
import datetime
import matplotlib.pyplot as plt
import os
import csv
import shutil
import matplotlib
matplotlib.use("Agg")

TRAINING_UPDATE_FREQUENCY = 1000
RUN_UPDATE_FREQUENCY = 10


class Logger():
    def __init__(self, header, directory_path):
        self.header = header
        self.directory_path = directory_path + self.timestamp() + "/"

        self.score = []
        self.step = []
        self.loss = []
        self.accuracy = []
        self.q = []

        if os.path.exists(self.directory_path):
            shutil.rmtree(self.directory_path, ignore_errors=True)
        os.makedirs(self.directory_path)

    def timestamp(self):
        return str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))

    def add_gameover(self, gameover):
        if gameover % RUN_UPDATE_FREQUENCY == 0:
            print('{{"metric": "gameover", "value": {}}}'.format(gameover))

    def add_score(self, value):
        self.score.append(value)
        if len(self.score) % RUN_UPDATE_FREQUENCY == 0:
            self.save_log(self.score, "gameover", "score",
                          RUN_UPDATE_FREQUENCY, self.directory_path, self.header)
            self.score = []

    def add_step(self, value):
        self.step.append(value)
        if len(self.step) % RUN_UPDATE_FREQUENCY == 0:
            self.save_log(self.step, "gameover", "number of steps",
                          RUN_UPDATE_FREQUENCY, self.directory_path, self.header)
            self.step = []

    def add_accuracy(self, value):
        self.accuracy.append(value)
        if len(self.accuracy) % TRAINING_UPDATE_FREQUENCY == 0:
            self.save_log(self.accuracy, "update", "accuracy",
                          TRAINING_UPDATE_FREQUENCY, self.directory_path, self.header)
            self.accuracy = []

    def add_loss(self, value):
        value = min(5, value)  # clip loss, max = 5
        self.loss.append(value)
        if len(self.loss) % TRAINING_UPDATE_FREQUENCY == 0:
            self.save_log(self.loss, "update", "loss",
                          TRAINING_UPDATE_FREQUENCY, self.directory_path, self.header)
            self.loss = []

    def save_log(self, values, x_label, y_label, update_frequency, directory_path, header):
        mean_value = np.mean(values)
        print(y_label + ": (min: " + str(min(values)) + ", avg: " +
              str(mean_value) + ", max: " + str(max(values)))
        print('{"metric": "' + y_label + '", "value": {}}}'.format(mean_value))
        self.save_data(self.directory_path + y_label + ".csv", mean_value)
        self.save_fig(input_path=self.directory_path + y_label + ".csv",
                      output_path=self.directory_path + y_label + ".png",
                      small_batch_length=update_frequency,
                      x_label=x_label,
                      y_label=y_label)

    def save_fig(self, input_path, output_path, small_batch_length, big_batch_length, x_label, y_label):
        x = []
        y = []
        with open(input_path, "r") as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for i in range(0, len(data)):
                x.append(float(i)*small_batch_length)
                y.append(float(data[i][0]))

        plt.subplots()
        plt.plot(x, y, label="last " + str(small_batch_length) + " average")

        plt.title(self.header)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()

    def save_data(self, path, score):
        if not os.path.exists(path):
            with open(path, "w"):
                pass
        scores_file = open(path, "a")
        with scores_file:
            writer = csv.writer(scores_file)
            writer.writerow([score])
