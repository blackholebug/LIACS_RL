from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense


class CNN():
    def __init__(self, input_shape, action_space, is_dueling=False):
        self.input_shape = input_shape
        self.action_space = action_space
        self.optimizer = RMSprop(lr=0.00025, rho=0.95, epsilon=0.01)
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, 8,
                         strides=(4, 4),
                         padding="valid",
                         activation="relu",
                         input_shape=self.input_shape,
                         data_format="channels_first"))
        model.add(Conv2D(64, 4,
                         strides=(2, 2),
                         padding="valid",
                         activation="relu",
                         input_shape=self.input_shape,
                         data_format="channels_first"))
        model.add(Conv2D(64, 3,
                         strides=(1, 1),
                         padding="valid",
                         activation="relu",
                         input_shape=self.input_shape,
                         data_format="channels_first"))
        model.add(Flatten())
        model.add(Dense(512, activation="relu"))
        model.add(Dense(self.action_space))
        model.compile(loss="mse",
                      optimizer=self.optimizer,
                      metrics=["accuracy"])
        model.summary()
        return model
