# cassie-rl
An OpenAI Gym style reinforcement learning interface for Agility Robotics' biped robot Cassie 

# Installation

1.  Place ```mjpro150/``` and ```mjkey.txt``` in the ```cassie/cassiemujoco``` folder (see http://www.mujoco.org/ for info on downloading MuJoCo and obtaining a license). 
2.  Place ```libcassiemujoco.so``` in the ```cassie/cassiemujoco``` folder (see https://github.com/osudrl/cassie-mujoco-sim for info on compiling libcassiemujoco.so).
3.  Run ```$ pip install -e .``` in root folder (the one that contains setup.py). 

# TODO:

Add the OpenAI gym environment registration code so that the environment can be created with gym.make().
