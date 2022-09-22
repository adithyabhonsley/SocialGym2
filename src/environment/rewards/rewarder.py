from typing import List, Tuple, Dict, TYPE_CHECKING

import numpy as np
from tensorboardX import SummaryWriter

from src.environment.rewards import Reward

if TYPE_CHECKING:
    from src.environment.ros_social_gym import RosSocialEnv


class Rewarder:
    """
    Class that handles storing reward classes, calling them to sum their reward, and logging if a logger is given.
    """

    registered_rewards: List[Reward]

    __step_idx__: int

    def __init__(
            self,
            registered_rewards: List[Reward],
    ):
        """
        :param registered_rewards: The reward class objects to run each timestep of the environment
        :param tbx_writer: TensorboardX Summary Writer used for logging
        """

        self.registered_rewards = registered_rewards

    def reward(
            self,
            env: 'RosSocialEnv',
            observation_map,
            data_map
    ) -> Tuple[np.array, Dict[str, float]]:
        """
        Given the environments response for the current timestep, calculate the total reward (sum of all the registered
        reward class objects) and log the individual rewards as well as the total reward if the tensorboardX Summary
        Writer is present.

        :param env: The RosSocialEnv being used in the current episode
        :param env_response: The response from the utmrsStepper
        :param data_map: Not really used TODO - figure out if this is necessary
        """

        total_reward = 0.
        reward_map = {}  # Build a map of reward names to reward values for the tensorboard logger.
        for reward_fn in self.registered_rewards:
            reward = reward_fn(env, observation_map, data_map)
            reward_map[reward_fn.name()] = reward
            total_reward += reward

        reward_map['total'] = total_reward

        return total_reward, reward_map

    def setup(self, env: 'RosSocialEnv'):
        """
        Helper for reward classes that require environment knowledge before being run.
        """

        [x.__setup__(env) for x in self.registered_rewards]
