from .cassiemujoco import pd_in_t, CassieSim, CassieVis

from .trajectory import CassieTrajectory

from math import floor

import numpy as np 
import os
import random

import gym
from gym import spaces
#import pickle

class CassieEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, simrate=60):

        self.sim = CassieSim()
        self.vis = None

        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self._get_obs().shape)
        self.action_space      = spaces.Box(low=-np.inf, high=np.inf, shape=(10,))

        self.P = np.array([100,  100,  88,  96,  50]) 
        self.D = np.array([10.0, 10.0, 8.0, 9.6, 5.0])

        self.u = pd_in_t()

        self.simrate = simrate # simulate X mujoco steps with same pd target
                               # 60 brings simulation from 2000Hz to roughly 30Hz

        self.time    = 0 # number of time steps in current episode

        self.init_qpos = np.copy(self.sim.qpos())
        self.init_qvel = np.copy(self.sim.qvel())

    @property
    def dt(self):
        return 1 / 2000 * self.simrate

    def close(self):
        if self.vis is not None:
            del self.vis # overloaded to call cassie_vis_free
            self.vis = None
    
    def step_simulation(self, action):
        target = action 

        self.u = pd_in_t()
        for i in range(5):
            self.u.leftLeg.motorPd.pGain[i]  = self.P[i]
            self.u.rightLeg.motorPd.pGain[i] = self.P[i]

            self.u.leftLeg.motorPd.dGain[i]  = self.D[i]
            self.u.rightLeg.motorPd.dGain[i] = self.D[i]

            self.u.leftLeg.motorPd.torque[i]  = 0 # Feedforward torque
            self.u.rightLeg.motorPd.torque[i] = 0 

            self.u.leftLeg.motorPd.pTarget[i]  = target[i]
            self.u.rightLeg.motorPd.pTarget[i] = target[i + 5]

            self.u.leftLeg.motorPd.dTarget[i]  = 0
            self.u.rightLeg.motorPd.dTarget[i] = 0

        self.sim.step_pd(self.u)

    def step(self, action):
        self.time  += 1

        pos_before = np.copy(self.sim.qpos())[0]

        for _ in range(self.simrate):
            self.step_simulation(action)

        pos_after = np.copy(self.sim.qpos())[0]

        reward = self._get_reward(pos_before, pos_after)

        # same as CassieMimicEnv
        height = self.sim.qpos()[2]
        done = bool((height < 0.4) or (height > 3.0))

        return self._get_obs(), reward, done, {}

    def reset(self):
        self.time = 0

        c = 0.01 # same as Gym Humanoid

        new_qpos = self.init_qpos + np.random.uniform(low=-c, high=c, size=self.init_qpos.size)
        new_qvel = self.init_qvel + np.random.uniform(low=-c, high=c, size=self.init_qvel.size)

        self.sim.set_qpos(new_qpos)
        self.sim.set_qvel(new_qvel)

        return self._get_obs()

    # deterministic reset
    def reset_for_test(self):
        self.time = 0

        self.sim.set_qpos(self.init_qpos)
        self.sim.set_qvel(self.init_qvel)

        return self._get_obs()
    
    def set_joint_pos(self, jpos, fbpos=None, iters=5000):
        """
        Kind of hackish. 
        This takes a floating base position and some joint positions
        and abuses the MuJoCo solver to get the constrained forward
        kinematics. 

        There might be a better way to do this, e.g. using mj_kinematics
        """

        # actuated joint indices
        joint_idx = [7, 8, 9, 14, 20,
                     21, 22, 23, 28, 34]

        # floating base indices
        fb_idx = [0, 1, 2, 3, 4, 5, 6]

        for _ in range(iters):
            qpos = np.copy(self.sim.qpos())
            qvel = np.copy(self.sim.qvel())

            qpos[joint_idx] = jpos

            if fbpos is not None:
                qpos[fb_idx] = fbpos

            self.sim.set_qpos(qpos)
            self.sim.set_qvel(0 * qvel)

            self.sim.step_pd(pd_in_t())


    # Essentially the same as Gym Humanoid
    def _get_reward(self, pos_before, pos_after):
        alive_bonus = 5.0
        lin_vel_cost = 1.25 * (pos_after - pos_before) / self.dt
        quad_ctrl_cost = 0 # TODO
        quad_impact_cost = 0 # TODO
        quad_impact_cost = min(quad_impact_cost, 10)

        reward = lin_vel_cost - quad_ctrl_cost - quad_impact_cost + alive_bonus

        return reward


    def _get_obs(self):
        qpos = np.copy(self.sim.qpos())
        qvel = np.copy(self.sim.qvel()) 

        return np.concatenate([qpos[2:], 
                               qvel[:]])

    def render(self):
        if self.vis is None:
            self.vis = CassieVis()

        self.vis.draw(self.sim)
