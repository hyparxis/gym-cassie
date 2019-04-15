# gym-cassie
An OpenAI Gym reinforcement learning interface for Agility Robotics' biped robot Cassie.

# Installation
1. Install [OpenAI Gym](https://github.com/openai/gym)
2.  Place ```mjpro150/``` and ```mjkey.txt``` in the ```cassie/cassiemujoco``` folder (see http://www.mujoco.org/ for info on downloading MuJoCo and obtaining a license). 
3.  Place ```libcassiemujoco.so``` in the ```cassie/cassiemujoco``` folder (see https://github.com/osudrl/cassie-mujoco-sim for info on compiling libcassiemujoco.so). Temporary note: cassie-rl currently uses a different version of cassie-mujoco-sim with a foot position API. For now see my fork of the former here: https://github.com/p-morais/cassie-mujoco-sim.
4.  Run ```$ pip install -e .``` in root folder (the one that contains setup.py). 

To test installation:
```
$ python3
> from gym_cassie import CassieMimicEnv
> env = CassieMimicEnv("walking")
> env.render()
```
Alternatively:
```
$ python3
> import gym
> import gym_cassie
> env = gym.make("Cassie-v0")
> env.render()
> env.close()
```

# Environments
Cassie-v0: A "go forward" environment meant to be a close match to OpenAI gym's Humanoid environment in terms of state and reward.
Cassie-mimic-v0: A faithful reimplementation of the environment described in [Feedback Control For Cassie With Deep Reinforcement Learning](https://arxiv.org/abs/1803.05580). Also see [DeepMimic](https://arxiv.org/abs/1804.02717).

# TODO
* Add the option to use the Cassie state estimator output as the network input (this would allow policies to be run on the actual robot).
