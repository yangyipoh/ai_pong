# AI Pong
The following is the game of Pong with AI using Neural Evolution of Augmented Topologies.

## Usage
A regular game of Pong can be run using the following command
```
python main.py
```
To use the AI instead of manual control, the ```--network``` flag can be used. Note that ```network.pkl``` is needed in this case.
```
python main.py --network
```
## Training
To train a new neural network, the following line can be run
```
python train.py
```
Note that ```config.ini``` is needed.

To adjust the training parameters, open ```config.ini``` in any text editor. Full documentation on the hyperparameters can be found in the [NEAT-Python](https://neat-python.readthedocs.io/en/latest/#:~:text=NEAT%20is%20a%20method%20developed,as%20well%20as%20PyPy%203.) page.