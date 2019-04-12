# gym-cassie
An OpenAI Gym style reinforcement learning interface for Agility Robotics' biped robot Cassie. CassieEnv is a reimplementation of: https://arxiv.org/abs/1803.05580.

# Installation

1.  Place ```mjpro150/``` and ```mjkey.txt``` in the ```cassie/cassiemujoco``` folder (see http://www.mujoco.org/ for info on downloading MuJoCo and obtaining a license). 
2.  Place ```libcassiemujoco.so``` in the ```cassie/cassiemujoco``` folder (see https://github.com/osudrl/cassie-mujoco-sim for info on compiling libcassiemujoco.so). Temporary note: cassie-rl currently uses a different version of cassie-mujoco-sim with a foot position API. For now see my fork of the former here: https://github.com/p-morais/cassie-mujoco-sim.
3.  Run ```$ pip install -e .``` in root folder (the one that contains setup.py). 

To test installation:
```
$ python3
> from cassie import CassieEnv
> env = CassieEnv("walking")
> env.render()
```
