import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from tqdm import tqdm


def animation(x_pos, y_pos, duration, title, solar_system=False, save=True):
    """
    Creates an animation which shows the motion of the stars over time.

    Parameters
    ----------
    x_pos : np.Array of dimension 2
        Absissas of the stars over time.
    y_pos : np.Array of dimension 2
        Ordinates of the stars over time.
    duration : float
        Total duration on which are computed the positions (in years).
    title : str
        Title of the graph and of the gif file of the animation 
        (if save is set to True).
    solar_system : bool, optional
        Choose whether or not to trigger the legend and to display the stars
        as elements of the Solar system. The default is False.
    save : bool, optional
        Choose if the animation should be saved as a gif file. 
        The default is True.

    Returns
    -------
    None
    """
    colors = ['gold', 'green', 'orange', 'b', 'r', 'sandybrown', 
              'moccasin', 'lightskyblue', 'mediumblue', 'hotpink']
    labels = ['Soleil', 'Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 
              'Saturne', 'Uranus', 'Neptune', 'Astre perturbateur']
    #initialise the animation
    def init():
        for line, star in zip(lines, stars):
            line.set_data([], [])
            star.set_data([], [])
        return lines + stars

    #updates the position of the elements at each frame
    def update(frame):
        for n, (line, star) in enumerate(zip(lines, stars)):
            line.set_data(x_pos[n, :frame], y_pos[n, :frame]) 
            star.set_data(x_pos[n, 0], y_pos[n, 0])  
        #dynamically adjust x and y axis limits based on the range of the displayed data
        try: #to avoid looking for a minimum in an empty set
            ax.set_xlim(np.min(x_pos[:, :frame]), np.max(x_pos[:, :frame]))
            ax.set_ylim(np.min(y_pos[:, :frame]), np.max(y_pos[:, :frame]))
        except ValueError:
            pass
        return lines + stars
    
    #setup an empty figure
    fig, ax = plt.subplots()
    plt.grid()
    N, nb_steps = x_pos.shape
    lines = [ax.plot([], [], '-', marker='+', markersize=10, markevery=[-1], color=colors[n])[0] for n in range(N)]  #create empty lines with markers
    stars = [ax.plot([], [], '*', markersize=10, color=colors[n])[0] for n in range(N)]  #create stars
    #set the labels and display the legend (if we are animating the solar system)
    for line, label in zip(lines, labels):
        line.set_label(label)
    if solar_system:
        ax.legend()
    #plot the animation and set the title
    print('Plotting animation...')
    ani = FuncAnimation(fig, update, frames=tqdm(range(nb_steps)), init_func=init, interval=duration, blit=True)
    plt.title(title)
    #save the animation as a gif file
    if save:
        ani.save(title + '.gif', writer='pillow')
        print('Animation saved as ' + title + '.gif')
    #display the animation
    plt.show()