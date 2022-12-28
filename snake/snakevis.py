import matplotlib.pyplot as plt
import time
import gym

from gym import envs
print(envs.registry.keys())

env = gym.make("snake:SnakeEnv-v0")

env.reset()
env.render("human")
action = env.action_space.sample()
img, reward, done, info = env.step(action)
plt.figure()
plt.imshow(img)

