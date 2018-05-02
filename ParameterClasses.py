from enum import Enum
import Younger_InputData as Data
import scr.RandomVariantGenerators as Random
import scr.FittingProbDist_MM as Est


class HealthStats(Enum):
    """ health states of patients with HIV """
    HIGH_RISK = 0
    DIAGNOSIS = 1
    LUNG_DEATH = 2
    NON_LUNG_DEATH = 3


class Therapies(Enum):
    """ LDCT vs. PLCO screening test """
    LDCT = 0
    PLCO = 1


class _Parameters():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.HIGH_RISK

        # annual treatment cost
        if self._therapy == Therapies.LDCT:
            self._annualTreatmentCost = Data.LDCT_COST
        else:
            self._annualTreatmentCost = Data.PLCO_COST

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # annual state costs and utilities
        self._annualStateCosts = []
        self._annualStateUtilities = []

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.LUNG_DEATH or state == HealthStats.NON_LUNG_DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.LUNG_DEATH or state == HealthStats.NON_LUNG_DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost


class ParametersFixed(_Parameters):
    def __init__(self, therapy):

        # initialize the base class

        _Parameters.__init__(self, therapy)

        if self._therapy == Therapies.LDCT:
            # calculate transition probabilities depending of which screening test is used
            self._prob_matrix = Data.TRANS_MATRIX_LDCT
        else:
            self._prob_matrix = Data.TRANS_MATRIX_PLCO


        # annual state costs and utilities
        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

class ParametersProbabilistic(_Parameters):

    def __init__(self, seed, therapy):

        # initializing the base class
        _Parameters.__init__(self, therapy)

        self._rng = Random.RNG(seed)    # random number generator to sample from parameter distributions
        self._hivProbMatrixRVG_LDCT = []  # list of dirichlet distributions for transition probabilities of LDCT
        self._hivProbMatrixRVG_PLCO = []
        #self._lnRelativeRiskRVG = None  # random variate generator for the natural log of the treatment relative risk
        self._annualStateCostRVG = []       # list of random variate generators for the annual cost of states
        self._annualStateUtilityRVG = []    # list of random variate generators for the annual utility of states

        # HIV transition probabilities
        j = 0
        for prob in Data.TRANS_MATRIX_LDCT:
            self._hivProbMatrixRVG_LDCT.append(Random.Dirichlet(prob[j:]))
            j += 1   # you should make sure everything you use is not "0" in the dirichlet
        for prob in Data.TRANS_MATRIX_PLCO:
            self._hivProbMatrixRVG_PLCO.append(Random.Dirichlet(prob[j:]))
            j += 1
        # treatment relative risk
        # find the mean and st_dev of the normal distribution assumed for ln(RR)


        # annual state cost, we assume gamma distribution
        for cost in Data.ANNUAL_STATE_COST:
            # find shape and scale of the assumed gamma distribution
            estDic = Est.get_gamma_params(mean=cost, st_dev=cost / 4)
            # append the distribution
            self._annualStateCostRVG.append(Random.Gamma(a=estDic["a"], loc=0, scale=estDic["scale"]))

        # annual state utility, we assume beta distribution
        for utility in Data.ANNUAL_STATE_UTILITY:
            # find alpha and beta of the assumed beta distribution
            estDic = Est.get_beta_params(mean=utility, st_dev=utility / 4)
            # append the distribution
            self._annualStateUtilityRVG.append(
                Random.Beta(a=estDic["a"], b=estDic["b"]))

        # we need to sample from lists above
    def __resample(self):

            # calculate transition probabilities
            # create an empty matrix populated with zeroes
            self._prob_matrix = []
            for s in HealthStats:
                self._prob_matrix.append([0] * len(HealthStats))

            # for all health states
            for s in HealthStats:
                # if the current state is death
                if s in [HealthStats.HIV_DEATH, HealthStats.BACKGROUND_DEATH]:
                    # the probability of staying in this state is 1
                    self._prob_matrix[s.value][s.value] = 1
                elif self._therapy == Therapies.LDCT:
                    # sample from the dirichlet distribution to find the transition probabilities between hiv states
                    sample = self._hivProbMatrixRVG_LDCT[s.value].sample(self._rng)
                    for j in range(len(sample)):
                        self._prob_matrix[s.value][s.value + j] = sample[j]
                elif self._therapy == Therapies.PLCO:
                    sample = self._hivProbMatrixRVG_PLCO[s.value].sample(self._rng)
                    for j in range(len(sample)):
                        self._prob_matrix[s.value][s.value + j] = sample[j]

          # sample from gamma distributions that are assumed for annual state costs
            self._annualStateCosts = []
            for dist in self._annualStateCostRVG:
                self._annualStateCosts.append(dist.sample(self._rng)) # sample by passing the number generator

            # sample from beta distributions that are assumed for annual state utilities
            self._annualStateUtilities = []
            for dist in self._annualStateUtilityRVG:
                self._annualStateUtilities.append(dist.sample(self._rng))


