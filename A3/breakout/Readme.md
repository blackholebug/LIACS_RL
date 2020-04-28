# Instruction
To run the program, please use tensorflow 1.x as the backend. Our implementation is based on tensorflow 1.15. 
Please run `python main.py` under the folder.  There are many parameters to turn in this program. We list the most important parameters in `args.py` for tweaking. 

# Structure

The main loop for training or testing is in `main.py`, which is also an entry for this program. The wrapped environment is produced by `wrapped_env.py`. In the main loop, the program will initialize a model by training a new one, or loading a trained model from a given path. The model is defined in `dqn_model.py`.  The model will initialize one or two neural networks using `neural_network.py`. The `replay_memory.py` is called when the model is initialized and updated when the next action is executed. 