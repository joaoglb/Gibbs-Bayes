# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 02:45:45 2018

@author: User
"""

##Bliblioteca Guassiana
#from sklearn.naive_bayes import GaussianNB
import numpy as np
#from seaborn import plt
import pandas as pd
#plt.rcParams['figure.figsize'] = (10, 5)
#Verifica o lugar onde esta salvo o arquivo
#import os
#cwd = os.getcwd()
#print(cwd)
#Importar do Excel
import xlrd
book = xlrd.open_workbook("Teste_Vidro_04-05..xlsx")
sh = book.sheet_by_index(0)
RI = []
Na = []
Mg = []
#limite 215
sit = 215
for i in range(1,sit):
      RI.append(sh.cell(rowx=i,colx=1).value)
      Na.append(sh.cell(rowx=i,colx=2).value)
      Mg.append(sh.cell(rowx=i,colx=3).value)
y = np.array(RI)
V_Na = np.array(Na)
V_Mg = np.array(Mg)
x = np.stack((V_Mg,V_Na),axis=-1)

print(y)

def sample_beta_0(y, x, beta_1, tau, mu_0, tau_0):
    N = len(y)
    assert len(x) == N
    precision = tau_0 + tau * N
    mean = tau_0 * mu_0 + tau * np.sum(y - beta_1 * x)
    mean /= precision
    return np.random.normal(mean, 1 / np.sqrt(precision))

def sample_beta_1(y, x, beta_0, tau, mu_1, tau_1):
    N = len(y)
    assert len(x) == N
    precision = tau_1 + tau * np.sum(x * x)
    mean = tau_1 * mu_1 + tau * np.sum( (y - beta_0) * x)
    mean /= precision
    return np.random.normal(mean, 1 / np.sqrt(precision))

def sample_tau(y, x, beta_0, beta_1, alpha, beta):
    N = len(y)
    alpha_new = alpha + N / 2
    resid = y - beta_0 - beta_1 * x
    beta_new = beta + np.sum(resid * resid) / 2
    return np.random.gamma(alpha_new, 1 / beta_new)

beta_0_true = -1
beta_1_true = 2
tau_true = 1

#synth_plot = plt.plot(x, y, "o")
#plt.xlabel("x")
#plt.ylabel("y")

## specify initial values
init = {"beta_0": 0,
        "beta_1": 0,
        "tau": 2}

## specify hyper parameters
hypers = {"mu_0": 0,
         "tau_0": 1,
         "mu_1": 0,
         "tau_1": 1,
         "alpha": 2,
         "beta": 1}

def gibbs(y, x, iters, init, hypers):
    assert len(y) == len(x)
    beta_0 = init["beta_0"]
    beta_1 = init["beta_1"]
    tau = init["tau"]
    
    trace = np.zeros((iters, 3)) ## trace to store values of beta_0, beta_1, tau
    
    for it in range(iters):
        beta_0 = sample_beta_0(y, x, beta_1, tau, hypers["mu_0"], hypers["tau_0"])
        beta_1 = sample_beta_1(y, x, beta_0, tau, hypers["mu_1"], hypers["tau_1"])
        tau = sample_tau(y, x, beta_0, beta_1, hypers["alpha"], hypers["beta"])
        trace[it,:] = np.array((beta_0, beta_1, tau))
        
    trace = pd.DataFrame(trace)
    trace.columns = ['beta_0', 'beta_1', 'tau']
        
    return trace

iters = 1000
trace = gibbs(y, x, iters, init, hypers)

traceplot = trace.plot()
traceplot.set_xlabel("Iteration")
traceplot.set_ylabel("Parameter value")

trace_burnt = trace[500:999]
hist_plot = trace_burnt.hist(bins = 30, layout = (1,3))

print(trace_burnt.median())
print(trace_burnt.std())