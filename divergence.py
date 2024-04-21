import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import random
from tqdm import tqdm

import get_positions, init

def check_DV(x_pos, y_pos, treshold=10**3):
    """
    Check if a system is considered as divergent.

    Parameters
    ----------
    x_pos : np.Array of dimension 2
        Absissas of the stars over time.
    y_pos : np.Array of dimension 2
        Ordinates of the stars over time.
    treshold : float, optional
        Treshold at which the system is considered divergent (in AU). 
        The default is 10**3.

    Returns
    -------
    bool
        True if the system has reached the treshold.

    """
    return max(np.max(np.abs(x_pos)), np.max(np.abs(y_pos))) > treshold


def get_DV_time(sim, duration, nb_steps=100, treshold=10**3):
    """
    Gives the smallest time at which the system is beyond the treshold.

    Parameters
    ----------
    sim : rebound simulation
        Contains all the data of the system.
    duration : float
        Maximum duration on which the computation are made.
        If the system is stable for the whole duration, the duration will be
        returned.
    nb_steps : int, optional
        Number of times the program checks if the system is beyond the treshold.
        Should be increased to improve the accuracy of the program.
        The default is 100.
    treshold : float, optional
        Treshold at which the system is considered divergent. 
        The default is 10**3.

    Returns
    -------
    t : float
        Time at which the system reaches the treshold.

    """
    vec_t = np.linspace(0, duration, num=nb_steps+1)
    for t in vec_t:
        x_pos, y_pos = get_positions.get_positions(sim, t, nb_steps=2, 
                                              verbose=False)
        if check_DV(x_pos, y_pos, treshold=treshold):
            return t
    #If the system is not detected as divergent, return the final time
    return t




def save_array(array, name, save_plot=True, verbose=True):
    """
    Save an array as a csv file.

    Parameters
    ----------
    array : np.array
        Array which should be saved.
    name : str
        Name of the file in which the array will be saved.
    save_plot : bool, optional
        Choose if the plot should be saved too. The default is True.
    verbose : bool, optional
        Choose if a message should be printed on the console to confirm that
        the array/plot is well saved. The default is True.

    Returns
    -------
    None.

    """
    rd_numbers = ''.join([random.choice('0123456789') for _ in range(12)])
    np.savetxt(rf"C:\Users\trist\Desktop\N_body\Arrays\{name}-{rd_numbers}.csv", array, delimiter=",")
    if save_plot:
        plt.savefig(rf"C:\Users\trist\Desktop\N_body\Arrays\{name}-{rd_numbers}.png")
    if verbose:
        print(f'array sauvegardé comme {name}-{rd_numbers}.csv')
        if save_plot:
            print(f'plot sauvegardé comme {name}-{rd_numbers}.png')
            
            
            
def plot_DV(func_init, m_min, m_max, m_step, p2_min, p2_max, p2_step, 
            duration=1000, treshold=10**3, size_nb=12, nb_steps=100):
    """
    Plot a heatmap that shows the divergence time for a given initialisaiton
    depending on the mass of the stars and on another parameter.

    Parameters
    ----------
    func_init : str
        Key to precise the initialisation fonction (see the init module).
    m_min : float
        Minimal mass of the stars.
    m_max : float
        Maximal mass of the stars.
    m_step : int
        Number of steps for the mass parameter.
    p2_min : float
        Minimal value for the second parameter.
    p2_max : float
        Maximal value for the second parameter.
    p2_step : int
        Number of steps for the second parameter.
    duration : float, optional
        Maximal duration on which the computations are made (in years). 
        The default is 100.
    treshold : float, optional
        Treshold at which the system is considered divergent. 
        The default is 10**3.
    size_nb : float, optional
        Size of the numbers displayed in the heatmap.
        The default is 12.
    nb_steps : int, optional
        Number of times the program checks if the system is beyond the treshold.
        Should be increased to improve the accuracy of the program.
        The default is 100.

    Returns
    -------
    vec_DV : array of dimension 2
        Divergence time with respect with both parameters.

    """
    dic_init = {'triangle':lambda m, p2: init.triangle(m, v0=p2),
                'perturbateur Système solaire':init.solar_syst_perturbator}
    dic_param2 = {'triangle':'Vitesse initiale (yr2pi)',
                  'perturbateur Système solaire':'Distance au soleil (UA)'}
    
    vec_m = np.arange(m_min, m_max, m_step)
    vec_p2 = np.arange(p2_min, p2_max, p2_step)
    vec_DV = np.zeros((len(vec_m), len(vec_p2)))
    for i,m in enumerate(tqdm(vec_m)):
        for j,p2 in enumerate(vec_p2):
            sim = dic_init[func_init](m, p2)
            temps_DV = get_DV_time(sim, duration, treshold=treshold, 
                                   nb_steps=nb_steps)
            vec_DV[i,j] = temps_DV
    draw_heatmap(vec_DV, np.array(vec_p2), vec_m, size_nb=size_nb)
    plt.title(f'Etude du temps de divergence du système ({func_init})')
    plt.xlabel(dic_param2[func_init])
    plt.ylabel('Masse (masses solaire)')
    save_array(vec_DV, func_init)
    plt.show()
    return vec_DV


def draw_heatmap(vec_data, vec_x, vec_y, size_nb=12):
    sns.heatmap(vec_data, xticklabels=np.array(vec_x), yticklabels=vec_y, 
                cbar=False, annot=True, norm=LogNorm(), annot_kws={"size": 12})
    plt.show()