from gym.envs.registration import register

register(
    id="SnakeEnv-v0",
    entry_point="snake.envs:SnakeEnv"
)