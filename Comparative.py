import Parameter as P
import MarkovModelClasses as MarkovCls
import SupportMarkovModel as SupportMarkov


# simulating mono therapy
# create a cohort
cohort_LDCT = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.LDCT)
# simulate the cohort
simOutputs_LDCT = cohort_LDCT.simulate()

# simulating combination therapy
# create a cohort
cohort_PLCO = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.PLCO)
# simulate the cohort
simOutputs_PLCO = cohort_PLCO.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_LDCT, simOutputs_PLCO)

# print the estimates for the mean survival time and mean time to AIDS
SupportMarkov.print_outcomes(simOutputs_LDCT, "LDCT Screening:")
SupportMarkov.print_outcomes(simOutputs_PLCO, "PLCO Screening:")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_LDCT, simOutputs_PLCO)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_LDCT, simOutputs_PLCO)
