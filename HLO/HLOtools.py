# -*- coding: utf-8 -*-
"""
Created on Mon Dec 04 10:13:10 2017

@author: PJ
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def generate(popSize,m):
    '''
    generate a random Individual for HLO
    '''
    Bpop = np.random.randint(2,size=(popSize,m))
    return Bpop

def B2R(popSize,Bpop,dim,bit,bound):
    '''
    convert binary indivdual to real code format
    '''
    Rpop = np.zeros((popSize,dim))
    for i in range(0,popSize):
        for d in range(0,dim):
            for j in range(d*bit,(d+1)*bit):
                Rpop[i,d] = Rpop[i,d] + (Bpop[i,j]*2**((d+1)*bit-j-1))
            Rpop[i,d] = bound[0]+(bound[1]-bound[0])*Rpop[i,d]/(2**bit-1)
    return Rpop

def Evfit(Rpop,dim):
    """
    sphere function
    """
    o=sio.loadmat('sphere_func_data')
    o = o['o'].reshape(-1)
    f = np.zeros((len(Rpop)))
    for i in range(0,len(Rpop)):
        for j in range(0,dim):
            f[i] = f[i] + (Rpop[i,j]-o[j])**2
    return f

def printResult(Gmax,trace):
    '''
    plot the result of the HLO
    '''
    x = np.arange(0, Gmax)
    y1 = trace[:, 0]
    plt.plot(x, y1, 'r', label='optimal value')
    plt.xlabel("Iteration")
    plt.ylabel("function value")
    plt.title("HLO for function optimization")
    plt.legend()
    plt.show() 
        
       