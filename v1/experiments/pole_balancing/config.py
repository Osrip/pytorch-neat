import torch
import gym
from v1.phenotype.feed_forward import FeedForwardNet


class PoleBalanceConfig:
    DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    VERBOSE = True

    # Corresponds to https://github.com/openai/gym/wiki/CartPole-v0
    NUM_INPUTS = 4
    NUM_OUTPUTS = 1
    USE_BIAS = True

    ACTIVATION = 'sigmoid'
    SCALE_ACTIVATION = 4.9

    FITNESS_THRESHOLD = 100000.0

    POPULATION_SIZE = 150
    NUMBER_OF_GENERATIONS = 150
    SPECIATION_THRESHOLD = 3.0

    CONNECTION_MUTATION_RATE = 0.80
    CONNECTION_PERTURBATION_RATE = 0.90
    ADD_NODE_MUTATION_RATE = 0.03
    ADD_CONNECTION_MUTATION_RATE = 0.5

    CROSSOVER_REENABLE_CONNECTION_GENE_RATE = 0.25

    # Top percentage of species to be saved before mating
    PERCENTAGE_TO_SAVE = 0.80

    # Allow episode lengths of > than 200
    gym.envs.register(
        id='LongCartPole-v0',
        entry_point='gym.envs.classic_control:CartPoleEnv',
        max_episode_steps=100000
    )

    def fitness_fn(self, genome):
        # OpenAI Gym
        env = gym.make('LongCartPole-v0')
        done = False
        observation = env.reset()

        fitness = 0
        phenotype = FeedForwardNet(genome, self)

        while not done:
            input = torch.Tensor([observation]).to(self.DEVICE)

            pred = round(float(phenotype(input)))
            observation, reward, done, info = env.step(pred)

            fitness += reward
        env.close()

        return fitness
