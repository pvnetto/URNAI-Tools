# URNAI-Tools
URNAI Tools is a modular Deep Reinforcement Learning library that supports multiple environments, such as [PySC2](https://github.com/deepmind/pysc2), [OpenAI Gym](https://github.com/openai/gym), and [PyGame Learning Environment](https://github.com/ntasfi/PyGame-Learning-Environment). The main goal of URNAI Tools is to provide an easy way to develop DRL agents in a way that allows the developer to reuse as much code as possible when developing different agents, and that also allows him to reuse previously implemented models in different environments and to integrate new environments easily when necessary. The main advantage of using URNAI Tools is that the models you make for one environment will also work in other environments, so you can prototype new agents for different environments very easily.

## Getting Started

Follow these instructions to get a working copy of the project on your PC. It's a good idea to use the 'solve_x.py' files as a base to start developing your own agents.

### Prerequisites

- Python 3.6
- Numpy
- Pandas
- TensorFlow
- Keras

### Optional

You might need to install some of those depending on the environments you're going to use.

- [PySC2](https://github.com/deepmind/pysc2)
- [OpenAI Gym](https://github.com/openai/gym)
- [PyGame Learning Environment](https://github.com/ntasfi/PyGame-Learning-Environment)

### Installing

Run these commands on the terminal to install URNAI Tools on your computer.

```
cd 'your/save/path'
git clone https://github.com/pvnetto/URNAI-Tools.git
```

### Running the examples

To execute any of the examples we've included, just navigate to the project's folder and run them using Python.

```
cd 'project/save/path'
python solve_x.py
```

## Guide

Follow these instructions to start developing new stuff using our library.

### Building an agent for a supported environment

- Building a PySC2 agent
- Building an OpenAI Gym agent
- Building a PyGame Learning Environment agent

### Building a new DRL model

To build a new model, you should check the readme in the [urnai.models](https://github.com/pvnetto/URNAI-Tools/tree/master/urnai/models) module.

### Integrating a new environment

To integrate a new environment, you might want to check the readme in the [urnai.envs](https://github.com/pvnetto/URNAI-Tools/tree/master/urnai/envs) module.

## Roadmap

Here you'll find all the things that we plan to do in this project. **Bold** items are work in progress.

* [ ] Documentation
  * [ ] Core codebase documentation/commenting
  * [ ] **Documentation for each of the main modules (env, agents, models etc)**
  * [ ] Statistics for solved problems
* [ ] Support for new environments
  * [ ] [Arcade Learning Environment](https://github.com/mgbellemare/Arcade-Learning-Environment)
  * [ ] [Gym Retro](https://github.com/openai/retro)
  * [X] [Vizdoom](https://github.com/mwydmuch/ViZDoom)
* [ ] More Deep RL algorithms
  * [X] Policy Gradient
  * [ ] **A3C**
  * [ ] Curiosity-Driven Learning
  * [ ] Proximal Policy Optimization
* [X] Core codebase improvements
  * [X] Logger class
  * [ ] Save model parameters (currently saves only the weights)
* [ ] Solve more problems
  * [X] Frozenlake
  * [X] Cartpole-V0
  * [X] Cartpole-V1
  * [X] Taxi-V2
  * [ ] Flappy Bird
  * [ ] **StarCraft II - Simple 64 Map - Very Easy difficulty**



## Authors

* **Francisco de Paiva Marques Netto** - *Initial work* - [pvnetto](https://github.com/pvnetto)