# Parameters for USA scenario
# from https://github.com/Maths-against-Malaria/COVID19_ADE_Model/blob/main/COVID19_ADE_model_USA.py
# adapted to superinfection model (additional/missing parameters)
# meaning of parameters see covidSR_parameters_old
# comments on the right:
# '# new': parameter differs from 'old';
# '# same': it is the same in 'old' and in ADE
# '# old': does not exist in the ADE scenario, same as in 'old'
# '# own': does not exist in the ADE scenario, changed to adapt to related values that are new

par = dict()
# par['N']: Population size
par['N'] = 331e6                # new
# par['days']: Simulation duration in days
par['days'] = 900               # new

# par['D']: Average duration
par['D'] = dict()
# par['D']['E']: of latency period
par['D']['E'] = 3.7             # same
# par['D']['P']: of podromal states
par['D']['P'] = 1               # same
# par['D']['I']: of early infectious states
par['D']['I'] = 5               # new
# par['D']['L']: of late-infectious states
par['D']['L'] = 5               # new
# par['D']['s']: of transient multi infection to multi-infected states
par['D']['s'] = 3.2             # old

# par['NErl']: Erlang states
par['NErl'] = dict()
par['NErl']['E'] = 16           # same
par['NErl']['P'] = 16           # same
par['NErl']['I'] = 16           # same
par['NErl']['L'] = 16           # same
par['NErl']['s'] = 16           # same

# Relative contagiousness
par['c'] = dict()
par['c']['P'] = 0.5             # same
par['c']['I'] = 1               # same
par['c']['L'] = 0.5             # new

# par['q']: Probability that single-infected lead to transient multi-infection
par['q'] = dict()
# in latent states
par['q']['E'] = 1               # same
# in podromal states
par['q']['P'] = 0.75            # same
# in fully contagious states
par['q']['I'] = 0.5             # same
# in late-infectious states
par['q']['L'] = 0.25            # same


par['R0'] = dict()
# Annual average basic reproduction number
par['R0']['R0bar'] = 3.2        # new
# Amplitude of the seasonal fluctuation of the basic reproduction number
par['R0']['a'] = 0.35           # new
# Day when R0 reaches its maximum
par['R0']['tR0max'] = 335       # new

# Fraction of contacts  that cause multi infections
## 'm' - related to multi-infections
## 's' - related to transient multi-infections
## '_' - related to single infections
par['m']=dict()
# with latent multi-infected
par['m']['_'] = 0               # old
# with multi infected
par['m']['m'] = 0.2             # old

# Fraction of symptomatic (sick) infections in fully contagious and late infectious states
par['fsick'] = dict()
# of single infections
par['fsick']['_'] = 0.58        # same
# of multi-infections
par['fsick']['m'] = 0.664       # old

# Fraction of sick who are die from the disease
par['fdead'] = dict()
# of single-infected
par['fdead']['_'] = 0.04        # new
# of multi-infected
par['fdead']['m'] = 0.05        # own

# No.  single infected in first fully contagious Erlang state  (they are in I_1, all others in S)
par['I1_0'] = 75                # new

# External force of infection
par['lExt'] = dict()
# leading to single infections
par['lExt']['_'] = 50           # old
# leading to multi-infections
par['lExt']['m'] = 0            # old

# Maximum capacity of the isolation units
par['Qmax'] = 30/10000 * par['N']  # new; wrong
# Prevented fraction of contacts of individuals who are isolated at home
par['phome'] = 0.75                 # same

# isolation:
# t: dates where measures change
# f_, fm: Prevented fraction of contacts because of general social-distancing measures in the time interval (f_: single, transient multiple; fm: multiple)
# (the first value is taken for any date before the first time and after the last one; else for t[i] <= t <= t[i+1] the value is f_[i+1], fm[i+1]
par['iso'] = dict()
# time intervals
par['iso']['t'] = [20,par['days']]
par['iso']['f_'] = [0,0.48]         # new
par['iso']['fm'] = [0,0.528]        # own

# general distancing
# (the first value is taken for any date before the first time and after the last one; else for t[i] <= t <= t[i+1] the value is p[i+1]
par['dist'] = dict()
par['dist']['t'] = [   50,  115,  190,  255,  290,  309,  316,  325,  335,  354,  450]  # new
par['dist']['p'] = [    0, 0.55, 0.22, 0.55, 0.45, 0.65, 0.55, 0.60, 0.70, 0.55, 0.65]  # new
# 0    # January  20, 2020  # Initial day of simulation
# 50   # March    10        # White house ban of gatherings (More than 10 persons)
# 115  # May      14        # State economic reopening + Black Lives Matter (BLM) protest
# 190  # July     28        # Experts warn for lockdowns necessity
# 255  # October  01        # BLM continues + schools reopening + campaigns
# 290  # November 05        # Lockdown
# 309  # November 24        # Thanksgiving period (more travels)
# 316  # December 01        # Less flights
# 325  # December 10        # Lockdowns (few flights)
# 335  # December 20        # Christmas period (family gatherings & more travels)
# 354  # January  08, 2021  # Post Christmas period
# 450  # April    15        #

par_newUSA = par
