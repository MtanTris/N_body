import numpy as np
from tqdm import tqdm


def get_positions(sim, duration, nb_steps=2, verbose=True):
    """
    Compute the position of the stars in the system over time.

    Parameters
    ----------
    sim : rebound simulation
        Contains all of the initial data of the system.
    duration : float.
        Total duration on which are computed the positions (in years).
    nb_steps : int, optional
        Number of steps taken in the computation. 
        The default is 2.
    verbose : bool, optional
        Choose if the progress bar should be printed.

    Returns
    -------
    x_pos : np.Array of dimension 2
        Absissas of the stars over time.
    y_pos : np.Array of dimension 2
        Ordinates of the stars over time.

    """
    #get the number of particles
    N = len(sim.particles)
    #setup the list of positions over time
    x_pos, y_pos = np.empty((N, nb_steps+1)), np.empty((N, nb_steps+1))
    vec_t = np.linspace(0, duration, nb_steps)
    #computing positions of the stars over time via integration of the system
    if verbose:
        print('Computing positions...')
        for i,t in tqdm(enumerate(vec_t)):
            sim.integrate(t)
            for n in range(N):
                x_pos[n, i] = sim.particles[n].x
                y_pos[n, i] = sim.particles[n].y
    else:
        for i,t in enumerate(vec_t):
            sim.integrate(t)
            for n in range(N):
                x_pos[n, i] = sim.particles[n].x
                y_pos[n, i] = sim.particles[n].y
    return x_pos, y_pos
