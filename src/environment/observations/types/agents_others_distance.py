import numpy as np

from src.environment.ros_social_gym import RosSocialEnv
from src.environment.observations import Observation
from src.environment.utils import poses_to_np_array


class AgentsOthersDistance(Observation):
    """
    Return the Normed distance between the agent and the other agents/humans
    """

    num_others: int

    def __init__(self):
        super().__init__()
        self.num_others = 0

    @classmethod
    def name(cls):
        return "agents_others_distance"

    def __len__(self):
        return self.num_others

    def __observations__(self, env: RosSocialEnv, env_response) -> np.array:
        others_pose = poses_to_np_array(env_response.human_poses).reshape((-1, 3))
        others_distances = np.linalg.norm(others_pose[:, 0:2], axis=-1)
        return others_distances

    def __setup__(self, env: RosSocialEnv):
        self.num_others = env.max_humans