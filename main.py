# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 14:40:23 2024

@author: trist
"""
import init, get_positions, plot, divergence

DURATION = 2000
NB_STEPS = DURATION*1


if __name__ == '__main__':
    #sim = init.triangle(11)
    #x_pos, y_pos = get_positions.get_positions(sim, DURATION, nb_steps=NB_STEPS)
    #plot.animation(x_pos, y_pos, DURATION, 'Tests', solar_system=False)
    divergence.plot_DV('triangle', 2, 30+2, 2, 0, 12+1, 1, duration=100000, 
                       treshold=10**3, nb_steps=1000)