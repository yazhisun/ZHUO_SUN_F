from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import Overall_InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random
import scr.FittingProbDist_MM as Est

class HealthStats(Enum):
    """ health states of patients with HIV """
    HIGH_RISK = 0
    EARLY_STAGE = 1
    LATE_STAGE = 2
    LUNG_DEATH = 3
    #NON_LUNG_DEATH = 4


class Therapies(Enum):
    """ mono vs. combination therapy """
    LDCT = 0
    PLCO = 1

class _Parameters:

    def __init__(self, therapy):
        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

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
        if state == HealthStats.LUNG_DEATH: #or state == HealthStats.NON_LUNG_DEATH:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.LUNG_DEATH: # or state == HealthStats.NON_LUNG_DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost

class ParametersFixed(_Parameters):
    def __init__(self, therapy):

        # initialize the base class
        _Parameters.__init__(self, therapy)

        # calculate transition probabilities depending of which therapy options is in use
        if self._therapy == Therapies.LDCT:
            # calculate transition probabilities depending of which screening test is used
            # calculate transition probabilities between hiv states
            self._prob_matrix = Data.TRANS_MATRIX_LDCT
        else:
            self._prob_matrix = Data.TRANS_MATRIX_PLCO

        # add background mortality if needed
        #if Data.ADD_BACKGROUND_MORT:
            #add_background_mortality(self._prob_matrix)

        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY

#def add_background_mortality(prob_matrix):

    # find the transition rate matrix
    #rate_matrix = MarkovCls.discrete_to_continuous(prob_matrix, 1)
    # add mortality rates
    #for s in HealthStats:
        #if s not in [HealthStats.LUNG_DEATH, HealthStats.NON_LUNG_DEATH]:
            #rate_matrix[s.value][HealthStats.NON_LUNG_DEATH.value] \
                    #= -np.log(1 - Data.ANNUAL_PROB_NONCANCER_MORT)

        # convert back to transition probability matrix
        #prob_matrix[:], p = MarkovCls.continuous_to_discrete(rate_matrix, Data.DELTA_T)
        # print('Upper bound on the probability of two transitions within delta_t:', p)
    #return [prob_matrix, p]

#



