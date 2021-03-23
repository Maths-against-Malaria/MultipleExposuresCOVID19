# the actual function to solve the system of differential equations
## takes all parameters in a dict (par)
## writes output to files with matching names:
## solution of differential equations: pathOut + "/covidSR_" + name + ".txt"
## parameters: pathOut + "/covidSR_" + name + "_par.txt"
## variables (lambda...) at all times: pathOut + "/covidSR_" + name + "_var.txt"

from covidSR_functions import *
from covidSR_differentialEquations import *
from scipy.integrate import solve_ivp

def modelSuperinfection(par, name, pathOut = 'results'):

    #truename = parToString(par)

    index = indexFunction(Nerls = par['NErl'])

    # to record the variables
    var_rec = [[-10000 for i in np.arange(11)] for j in np.arange(par['days'] + 1)]

    #print(name)
    # Initial values
    pop0 = [0 for i in np.arange(len(index))]

    # All individuals are susceptible, except those in I_1
    pop0[index['S']] = par['N'] - par['I1_0']
    pop0[index['I_1']] = par['I1_0']

    # Solve
    #timestartODE = datetime.datetime.now()

    def f(t, pop, par):

        # Initialize
        index = indexFunction(Nerls=par['NErl'])
        out = [0 for i in np.arange(len(index))]

        ## Variables
        var_t = varFunction(t, pop, par)
        var_rec[int(t)] = [t] + list(var_t.values())

        ## Compartments
        # Susceptible
        out[index['S']] = dS(pop, var_t, index)

        # E1
        out[index['E_1']] = dE1(pop, var_t, index)
        out[index['Es1']] = dEs1(pop, var_t, index)
        out[index['Em1']] = dEm1(pop, var_t, index)

        # E, P, I, L
        for i in np.arange(2, par['NErl']['E'] + 1): # E_2, ....E_nE
            ii = str(i)
            rates_i = rates('E', n=i, index=index, par=par, var=var_t)
            out[index['E_' + ii]] = d_(pop=pop, var=var_t, compartment='E', n=i, rates=rates_i, index=index, par=par)
            out[index['Es' + ii]] = ds(pop=pop, var=var_t, compartment='E', n=i, rates=rates_i, index=index, par=par)
            out[index['Em' + ii]] = dm(pop=pop, var=var_t, compartment='E', n=i, rates=rates_i, index=index, par=par)
        for i in np.arange(1, par['NErl']['P'] + 1):
            ii = str(i)
            rates_i = rates('P', n=i, index=index, par=par, var=var_t)
            out[index['P_' + ii]] = d_(pop=pop, var=var_t, compartment='P', n=i, rates=rates_i, index=index, par=par)
            out[index['Ps' + ii]] = ds(pop=pop, var=var_t, compartment='P', n=i, rates=rates_i, index=index, par=par)
            out[index['Pm' + ii]] = dm(pop=pop, var=var_t, compartment='P', n=i, rates=rates_i, index=index, par=par)
        for i in np.arange(1, par['NErl']['I'] + 1):
            ii = str(i)
            rates_i = rates('I', n=i, index=index, par=par, var=var_t)
            out[index['I_' + ii]] = d_(pop=pop, var=var_t, compartment='I', n=i, rates=rates_i, index=index, par=par)
            out[index['Is' + ii]] = ds(pop=pop, var=var_t, compartment='I', n=i, rates=rates_i, index=index, par=par)
            out[index['Im' + ii]] = dm(pop=pop, var=var_t, compartment='I', n=i, rates=rates_i, index=index, par=par)
        for i in np.arange(1, par['NErl']['L'] + 1):
            ii = str(i)
            rates_i = rates('L', n=i, index=index, par=par, var=var_t)
            out[index['L_' + ii]] = d_(pop=pop, var=var_t, compartment='L', n=i, rates=rates_i, index=index, par=par)
            out[index['Ls' + ii]] = ds(pop=pop, var=var_t, compartment='L', n=i, rates=rates_i, index=index, par=par)
            out[index['Lm' + ii]] = dm(pop=pop, var=var_t, compartment='L', n=i, rates=rates_i, index=index, par=par)

        out[index['D']] = dD(pop, var=var_t, par=par, index=index)
        out[index['R']] = dR(pop, var=var_t, par=par, index=index)
        return out

    # Solve system of differential equations
    soln = solve_ivp(f, [0,par['days']], pop0, method ="RK45",
                 t_eval = np.arange(0, par['days']),
                 dense_output = True,
                 args=[par])

    #timeendODE = datetime.datetime.now()
    np.savetxt(pathOut + "/covidSR_" + name + ".txt", soln.y)
    np.savetxt(pathOut + "/covidSR_" + name + "_var.txt", var_rec, fmt='%s')
    np.savetxt(pathOut + "/covidSR_" + name + "_par.txt", list(par.values()), fmt='%s')# [truename,' '] fmt ="%s"

    return name
