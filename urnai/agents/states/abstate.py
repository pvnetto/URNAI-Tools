from abc import ABC, abstractmethod
from agents.actions.base.abwrapper import ActionWrapper
from utils.types import *

class State(ABC):
    '''
    Every Agent needs to own an instance of this base class in order to define its State. So every time we want to create a new agent,
    we should either use an existing State implementation or create a new one.
    '''

    '''
    This method receives as a parameter an Observation and returns a State, which is usually a list of features extracted from the Observation. The Agent
    uses this State during training to receive a new action from its model and also to make it learn, that's why this method should always return a list.
    '''
    @abstractmethod
    def build_state(self, obs) -> List[Any]: ...

    '''
    Returns the dimensions of the States returned by the build_state method.
    '''
    @abstractmethod
    def get_state_dim(self):
        pass
