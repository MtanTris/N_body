import rebound
from numpy.random import rand

#Initialize the system : set the positions, masses and initiale speed of the stars


def triangle(M, v0=0, verbose=False):
    """
    Initialise a system of 3 stars, shaped in a a right-angled triangle of 
    length 3-4-5 and with equal inital velocity.

    Parameters
    ----------
    M : float
        Mass of the stars (in solar masses).
    v0 : float, optional
        Initial velocity of the stars, outwards from the system. 
        The default is 0.
    verbose : bool, optional
        Choose if the system status should be printed. The default is False.

    Returns
    -------
    sim : rebound simulation
        Contains all the data of the system.

    """
    sim = rebound.Simulation()
    sim.add(m=M)
    sim.add(m=M, x=3, y=0, vx=v0)
    sim.add(m=M, x=0, y=4, vy=v0)
    if verbose:
        sim.status()
    return sim

def solar_syst_perturbator(M, x, verbose=False):
    """
    Initialise a system composed of the solar system and a perturbator star.

    Parameters
    ----------
    M : float
        Mass of the perturbator star (in solar masses).
        If M is zero, then the perturbator star will not be put in the system.
    x : float
        Distance of the perutbator star from the Sun.
    verbose : bool, optional
        Choose if the system status should be printed. The default is False.

    Returns
    -------
    sim : rebound simulation
        Contains all the data of the system.

    """
    sim = rebound.Simulation()
    rebound.data.add_solar_system(sim)
    if M != 0:
        sim.add(m=M, x=x/2**.5, y=x/2**.5)
    if verbose:
        sim.status()
    return sim


def aligned(M, x, v0, verbose=False):
    """
    Initialise a system composed of 3 aligned stars, with equal distance
    between the outer stars and the one in the middle.

    Parameters
    ----------
    M : float
        Mass of the stars (in solar masses).
    x : float
        Distance between the outer stars and the one in the middle.
    v0 : float
        Initial speed of the outer stars, one upwards and one downwards.
    verbose : bool, optional
        Choose if the system status should be printed. The default is False.

    Returns
    -------
    sim : rebound simulation
        Contains all the data of the system.

    """
    sim = rebound.Simulation()
    sim.add(m=M)
    sim.add(m=M, x=x, vy=v0)
    sim.add(m=M, x=-x, vy=-v0)
    if verbose:
        sim.status()
    return sim


def equilateral(M, l, v0, verbose=False):
    """
    Initialise a system of 3 stars in the shape of an equilateral triangle.

    Parameters
    ----------
    M : float
        Mass of the stars (in solar masses).
    l : float
        Length of the edges of the triangle (in Sun-Earth distances).
    v0 : float
        Initial velocity of the stars, with a tangent direction from the smallest
        circle which encompasses the triangle.
    verbose : bool, optional
        Choose if the system status should be printed. The default is False.

    Returns
    -------
    sim : rebound simulation
        Contains all the data of the system.

    """
    sim = rebound.Simulation()
    sim.add(m=M, y=3**.5*l/4, vx=v0, vy=0)
    sim.add(m=M, x=-l/2, y=-3**.5*l/2, vx=-1/2*v0, vy=3**.5/2*v0)
    sim.add(m=M, x=l/2, y=-3**.5*l/2, vx=-1/2*v0, vy=-3**.5/2*v0)
    if verbose:
        sim.status()
    return sim


def random_two(M, m_range, x_range, v0_range, verbose=False):
    """
    Initialise a system of two stars with random characteristics.

    Parameters
    ----------
    M : float
        Mass of the first star.
    m_range : float
        Maximal difference between the masses of the two stars.
    x_range : float
        Maximal distance between the two stars.
    v0_range : float
        Maximal initial velocity of the second star.
    verbose : bool, optional
        Choose if the system status should be printed. The default is False.

    Returns
    -------
    sim : rebound simulation
        Contains all the data of the system.

    """
    sim = rebound.Simulation()
    sim.add(m=M)
    sim.add(m=M+m_range*rand(), x=x_range*rand(), vx=v0_range*rand())
    if verbose:
        sim.status()
    return sim