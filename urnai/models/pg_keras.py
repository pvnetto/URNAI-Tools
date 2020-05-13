import tensorflow as tf
import numpy as np
import random
import os
from collections import deque
from keras import Model
from keras.layers import Input, Dense, Conv2D, Flatten, MaxPooling2D 
from keras.optimizers import Adam
from keras import backend as K
from keras import utils as keras_utils

from .base.abmodel import LearningModel
from agents.actions.base.abwrapper import ActionWrapper
from agents.states.abstate import StateBuilder
from .model_builder import ModelBuilder
from urnai.utils.error import IncoherentBuildModelError

class PGKeras(LearningModel):

    def __init__(self, action_wrapper: ActionWrapper, state_builder: StateBuilder, learning_rate=0.002, gamma=0.95, 
                name='PolicyGradientKeras', build_model = ModelBuilder.DEFAULT_BUILD_MODEL):
        super(PGKeras, self).__init__(action_wrapper, state_builder, gamma, learning_rate, name, epsilon_min=0.1, epsilon_decay_rate=0.995)

        self.build_model = build_model
        self.model, self.predict_model = self.make_model()

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []
        
    def make_model(self):
        
        input = Input(shape=(self.state_size,))
        self.advantages = Input(shape=[1])
        dense1 = Dense(50, activation='relu')(input)
        dense2 = Dense(50, activation='relu')(dense1)
        output = Dense(self.action_size, activation='softmax')(dense2)

        model = Model(input=[input, self.advantages], output=[output])
        model.compile(optimizer=Adam(lr=self.learning_rate), loss=self.custom_loss)

        predict_model = Model(input=[input], output=[output])

        return model, predict_model

        # if self.build_model[0]['type'] == ModelBuilder.LAYER_INPUT and self.build_model[-1]['type'] == ModelBuilder.LAYER_OUTPUT:
        #     self.build_model[0]['shape'] = [None, self.state_size]
        #     self.build_model[-1]['length'] = self.action_size

        # for layer_model in self.build_model:
        #     if layer_model['type'] == ModelBuilder.LAYER_INPUT: 
        #         if self.build_model.index(layer_model) == 0:
        #             model.add(Dense(layer_model['nodes'], input_dim=layer_model['shape'][1], activation='relu'))
        #         else:
        #             raise IncoherentBuildModelError("Input Layer must be the first one.") 
        #     elif layer_model['type'] == ModelBuilder.LAYER_FULLY_CONNECTED:
        #         idx = self.build_model.index(layer_model) - 1 
        #         if self.build_model[idx]['type'] == ModelBuilder.LAYER_CONVOLUTIONAL:
        #             model.add(Flatten())

        #         model.add(Dense(layer_model['nodes'], activation='relu'))
        #     elif layer_model['type'] == ModelBuilder.LAYER_OUTPUT:
        #         idx = self.build_model.index(layer_model) - 1 
        #         if self.build_model[idx]['type'] == ModelBuilder.LAYER_CONVOLUTIONAL:
        #             model.add(Flatten())

        #         model.add(Dense(layer_model['length'], activation='linear'))
        #     elif layer_model['type'] == ModelBuilder.LAYER_CONVOLUTIONAL:
        #         if self.build_model.index(layer_model) == 0:
        #             model.add(Conv2D(layer_model['filters'], layer_model['filter_shape'], 
        #                       padding=layer_model['padding'], activation='relu', input_shape=layer_model['input_shape']))
        #             model.add(MaxPooling2D(pool_size=layer_model['max_pooling_pool_size_shape']))
        #         else:
        #             model.add(Conv2D(layer_model['filters'], layer_model['filter_shape'], 
        #                       padding=layer_model['padding'], activation='relu'))
        #             model.add(MaxPooling2D(pool_size=layer_model['max_pooling_pool_size_shape']))
        #     else:
        #         raise UnsupportedBuildModelLayerTypeError("Unsuported Layer Type " + layer_model['type'])

    def custom_loss(self, y_true, y_pred):
            out = K.clip(y_pred, 1e-8, 1-1e-8)
            log_likelyhood = y_true*K.log(out)
            
            return K.sum(-log_likelyhood*self.advantages)

    def memorize(self, state, action, reward):
        self.state_memory.append(state)
        self.action_memory.append(action)
        self.reward_memory.append(reward)

    def learn(self, s, a, r, s_, done, is_last_step: bool):
        self.memorize(s, a, r)

        if done or is_last_step:
            state_memory = np.array(self.state_memory)
            action_memory = np.array(self.action_memory)
            reward_memory = np.array(self.reward_memory)

            action_onehot = keras_utils.to_categorical(action_memory, num_classes=self.action_size)
            discount_reward = self.compute_discounted_R(reward_memory)

            actions = np.zeros([len(action_memory), self.action_size])
            actions[np.arange(len(action_memory)), action_memory] = 1

            G = np.zeros_like(reward_memory)
            for t in range(len(reward_memory)):
                G_sum = 0
                discount = 1
                for k in range(t, len(reward_memory)):
                    G_sum += reward_memory[k]*discount
                    discount *= self.gamma
                G[t] = G_sum
            mean = np.mean(G)
            std = np.std(G) if np.std(G) > 0 else 1
            G = (G-mean)/std

            self.model.train_on_batch([state_memory, G], actions)
            

    def compute_discounted_R(self, R):
        discounted_r = np.zeros_like(R, dtype=np.float32)
        running_add = 0
        for t in reversed(range(len(R))):
            running_add = running_add * self.gamma + R[t]
            discounted_r[t] = running_add

        discounted_r -= discounted_r.mean() / discounted_r.std()

        return discounted_r

    def choose_action(self, state, excluded_actions=[]):
        '''
        Choose Sction for policy gradient is equal as predict.
        Since there is no explore probability, all actions will come from the Net's weights.
        '''
        return self.predict(state)

    def save_extra(self, persist_path):
        # self.model.save(...)
        self.model.save(self.get_full_persistance_path(persist_path)+".h5")

    def load_extra(self, persist_path):
        exists = os.path.isfile(self.get_full_persistance_path(persist_path)+".h5")

        if(exists):
            self.model, self.predict_model = self.make_model()
            # self.model.load_model(...)
            self.model.load_weights(self.get_full_persistance_path(persist_path)+".h5")

    def predict(self, state, excluded_actions=[]):
        '''
        model.predict returns an array of arrays, containing the Q-Values for the actions. 
        This function uses the action probabilities from our policy to randomly select an action
        '''
        state = state[np.newaxis, :]
        action_prob = self.predict_model.predict(state)[0]
        action = np.random.choice(np.arange(self.action_size), p=action_prob)

        return action

    def ep_reset(self):
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []