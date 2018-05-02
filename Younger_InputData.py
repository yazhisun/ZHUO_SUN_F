
# simulation settings
POP_SIZE = 10000     # cohort population size
SIM_LENGTH = 20    # length of simulation (years) 55-75 years old
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

#ADD_BACKGROUND_MORT = True  # if background mortality should be added
DELTA_T = 1/4      # years

#PSA_ON = True      # if probabilistic sensitivity analysis is on

TRANS_MATRIX_PLCO = [
    [0.97942 , 0.015, 0.003, 0.00258],   # High-risk smoker without lung cancer
    [0,       0.55,   0.45, 0.0],   # positive Diagnosis with lung cancer
    [0,       0,      0.05, 0.95],  # early-stage
    [0,       0,      0.0, 1.0,],   # late-stage
    ]

# transition probability matrix for LDCT screening
TRANS_MATRIX_LDCT = [
    [0.97686, 0.0129, 0.00524, 0.0050],  # High-risk smoker without lung cancer
    [0, 0.55, 0.45, 0.0],  # positive Diagnosis with lung cancer
    [0, 0, 0.05, 0.95],  # early-stage
    [0, 0, 0.0, 1.0],# late-stage
]

# annual cost of each health state
ANNUAL_STATE_COST = [
    1703.20,# High-risk smoker without lung cancer
    16591,# Diagnosed with lung cancer
    40967
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1.00,   # High-risk smoker without lung cancer
    0.77,
    0.46
    ]
# annual screening test cost
LDCT_COST = 0
PLCO_COST = 0

# treatment relative risk
#TREATMENT_RR = 0.509
#TREATMENT_RR_CI = 0.365, 0.71  # lower 95% CI, upper 95% CI

# annual probability of non lung cancer caused mortality of old men who smoke much(number per year per 1,000 population)
#ANNUAL_PROB_NONCANCER_MORT = 37.07 / 1000

