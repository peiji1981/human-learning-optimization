#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 23:11:47 2017
@author: Ji Pei
% 1. This is a simple demo of HLO [1]. It is just tested by sphere function
% which is adopted in CEC'05.
% 2.This code defines the population size in 'popSize', number of design 
% generations in 'Gmax',current generation in 't'and bit number for each
% variable is 'bit'.
% 3.'bound' a list containing the lower and upper bounds of the design variables.
% 4.'pr'is the probability of random learning ,the values of (pi-pr) and
% (1-pi) represents the probabilities of performing individual learning and
% social learning, respectiely.
% 5.'IKD' is the individual knowledge database since the size of IKD=1 here;
% 'SKD' is the social knowledge database and the size of SKD is 1 in this demo.
% 6.For complicated problems, it highly recommends to introudce the re-learning
% operator given in [2] to obtain much better results.
% 7.HLO is sensitive to the parameters pr and pi. A simple adaptive strategy 
% is given in [3] to relieve the effort of parameter setting.

%% References:
% 1.Ling Wang, Haoqi Ni, Ruixin Yang, Minrui Fei, Wei Ye. A Simple Human Learnibg Optimization Algorithm. 
% Communications in Computer and Information Science. 2014 v462: 56-65
% 2.Ling Wang, Ruixin Yang, Haoqi Ni, Wei Ye, Minrui Fei, and Panos M. Pardalos. A Human Learning Optimization 
% Algorithm and Its Application to Multi-dimensional Knapsack Problems. Applied Soft Computing. 2015, 34: 736-743
% 3.Ling Wang, Haoqi Ni, Ruixin Yang, Panos M. Pardalos, Xin Du, Minrui Fei. An Adaptive Simplified Human 
% Learning Optimization Algorithm. Information Sciences. 2015, 320: 126-139

"""

import numpy as np
from HLOtools import *
import copy
    
class parameters:
    """
    set parameters for HLO
    """
    def __init__(self):

        self.bit = 30                 # Bits numbers
        self.dim = 2                  # Variable number
        self.m = self.bit*self.dim    # Individual lenth
        self.pr = 5.0/self.m          # pr
        self.pi = 0.85+2.0/self.m     # pi 
        self.bound = [-100,100]       # variable range
        self.popSize = 30             # the size of population
        self.Gmax = 200               # Max number of generations - stopping criteria 

class HLO(object):
    
    def __init__(self,P):
        self.pr = P.pr
        self.pi = P.pi
        self.bit = int(P.bit)
        self.dim = int(P.dim)
        self.bound = P.bound
        self.popSize = int(P.popSize)
        self.Gmax = int(P.Gmax)
        self.m = int(self.bit*self.dim)
        self.trace = np.empty((self.Gmax, 1))
        
        
    def initialization(self):
        '''
        initialization
        '''
        #initialize population
        self.Bpop = generate(self.popSize,self.m) 
        self.Rpop = B2R(self.popSize,self.Bpop,self.dim,self.bit,self.bound)
        self.fitness = Evfit(self.Rpop,self.dim)   

        #initialize ikd
        self.IKD = copy.deepcopy(self.Bpop)
        self.Pifit = copy.deepcopy(self.fitness)
        
        #initialize skd
        self.SKDfit = np.min(self.Pifit)
        bestIndex = np.argmin(self.Pifit)
        self.SKD = copy.deepcopy(self.IKD[bestIndex])
            
#        
    def RLO(self,pop):
        """
        random learning operator
        """
        if np.random.rand()<0.5:
            pop = 1
        else:
            pop = 0
            
        return pop
    
    def ILO(self,pop,IKD):
        """
        Individual learning operator
        """
        pop = IKD
        return pop
    
    def SLO(self,pop,SKD):
        """
        social learning operator
        """
        pop = SKD
        return pop
    
    def learning(self):
        '''
        learning process of HLO
        '''
        self.t=0
        self.initialization()
        self.trace[self.t, 0] = self.SKDfit
        print("Generation %d: optimal function value is: %f; "% (
            self.t, self.trace[self.t, 0]))
        
        while(self.t < self.Gmax - 1):
            for i in range(0,self.popSize):
                for j in range(0,self.m):
                    prob = np.random.rand()
                    #RLO
                    if prob<self.pr and prob>0:
                        self.Bpop[i,j] = self.RLO(self.Bpop[i,j])                        
                    #ILO
                    elif prob>=self.pr and prob<self.pi:
                        self.Bpop[i,j] = self.ILO(self.Bpop[i,j],self.IKD[i,j])
                    #SLO
                    elif prob>=self.pi and prob<1:
                        self.Bpop[i,j] = self.SLO(self.Bpop[i,j],self.SKD[j]) 
            
            # Evaluate new generation 
            self.Rpop = B2R(self.popSize,self.Bpop,self.dim,self.bit,self.bound)
            self.fitness = Evfit(self.Rpop,self.dim)
            
            # select IKD
            for i in range(0, self.popSize):
                if self.fitness[i] < self.Pifit[i]:
                    self.Pifit[i] = self.fitness[i]
                    self.IKD[i] = copy.deepcopy(self.Bpop[i])
            
            # select SKD
            best = np.min(self.Pifit)
            bestIndex = np.argmin(self.Pifit)
            if self.SKDfit > best:
                self.SKDfit = best
                self.SKD = copy.deepcopy(self.IKD[bestIndex])
                
            self.t +=1
            self.trace[self.t, 0] = self.SKDfit
            print("Generation %d: optimal function value is: %f; "% (
                    self.t, self.trace[self.t, 0]))
            
        print("Optimal function value is: %f; " % self.trace[self.t, 0])
        print("Optimal solution is:")
        print(self.SKD)
        printResult(self.Gmax,self.trace)
        return self.SKDfit

           
if __name__ == "__main__":
    
     P = parameters()
     b = HLO(P)
     best = b.learning()