import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import random
from src.particle import Particle
from src.test_functions import objective_function_1d

def run_pso_with_history():
    # PSO parameters
    max_iterations = 50
    num_particles = 10  # Using more particles for better visualization
    w, c1, c2 = 0.8, 0.1, 0.1  # Inertia weight and acceleration coefficients
    
    # Initialize particles
    particles_pool = [Particle(position=random.uniform(-100, 100), velocity=0) for i in range(num_particles)]
    
    # History storage
    position_history = []
    personal_best_history = []
    global_best_history = []
    
    # Initialize swarm best
    swarm_best_fitness = float('-inf')
    swarm_best_position = None
    
    # Initialize particles' best positions and fitness
    for particle in particles_pool:
        particle.fitness = -objective_function_1d(particle.position)
        particle.best_position = particle.position
        particle.best_fitness = particle.fitness
        
        if particle.fitness > swarm_best_fitness:
            swarm_best_fitness = particle.fitness
            swarm_best_position = particle.position
    
    # Save initial state
    positions = [p.position for p in particles_pool]
    personal_bests = [p.best_position for p in particles_pool]
    position_history.append(positions.copy())
    personal_best_history.append(personal_bests.copy())
    global_best_history.append(swarm_best_position)
    
    # Run PSO algorithm
    for iteration in range(max_iterations):
        for particle in particles_pool:
            # Update velocity and position
            new_velocity = (w * particle.velocity + 
                           c1 * random.random() * (particle.best_position - particle.position) + 
                           c2 * random.random() * (swarm_best_position - particle.position))
            new_position = particle.position + new_velocity
            
            particle.update_velocity(new_velocity)
            particle.position = new_position
            
            # Update fitness
            particle.fitness = -objective_function_1d(particle.position)
            
            # Update personal best
            if particle.fitness > particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = particle.position
            
            # Update swarm best
            if particle.fitness > swarm_best_fitness:
                swarm_best_fitness = particle.fitness
                swarm_best_position = particle.position
        
        # Save current state
        positions = [p.position for p in particles_pool]
        personal_bests = [p.best_position for p in particles_pool]
        position_history.append(positions.copy())
        personal_best_history.append(personal_bests.copy())
        global_best_history.append(swarm_best_position)
        
        print(f"Iteration {iteration + 1}/{max_iterations} completed.")
        print(f"Swarm best fitness: {swarm_best_fitness} at position {swarm_best_position}")
    
    return position_history, personal_best_history, global_best_history

def visualize_pso():
    # Get PSO history
    position_history, personal_best_history, global_best_history = run_pso_with_history()
    
    # Setup the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.25)
    
    # Plot the objective function for reference
    x = np.linspace(-100, 100, 1000)
    y = [-objective_function_1d(pos) for pos in x]
    ax.plot(x, y, 'k-', alpha=0.3, label='Objective Function')
    
    # Initial empty plots
    particles_scatter = ax.scatter([], [], c='blue', s=100, alpha=0.7, label='Particles')
    personal_best_scatter = ax.scatter([], [], c='green', s=50, alpha=0.7, label='Personal Best')
    global_best_scatter = ax.scatter([], [], c='red', s=150, marker='*', label='Global Best')
    
    # Set plot limits and labels
    ax.set_xlim(-100, 100)
    ax.set_ylim(min(y) - 1, max(y) + 10)
    ax.set_xlabel('Position')
    ax.set_ylabel('Fitness')
    ax.set_title('Particle Swarm Optimization - 1D')
    ax.legend()
    
    # Create a list to store arrow objects
    arrows = []
    
    # Animation function
    def animate(i):
        # Clear previous arrows
        for arrow in arrows:
            if arrow in ax.patches:
                arrow.remove()
        arrows.clear()
        
        positions = position_history[i]
        p_bests = personal_best_history[i]
        g_best = global_best_history[i]
        
        # Calculate fitness values
        fitness_values = [-objective_function_1d(p) for p in positions]
        pbest_fitness = [-objective_function_1d(p) for p in p_bests]
        gbest_fitness = -objective_function_1d(g_best)
        
        # Update particle positions
        particles_scatter.set_offsets(np.column_stack([positions, fitness_values]))
        
        # Update personal bests
        personal_best_scatter.set_offsets(np.column_stack([p_bests, pbest_fitness]))
        
        # Update global best
        global_best_scatter.set_offsets(np.array([[g_best, gbest_fitness]]))
        
        # Update title with iteration number
        ax.set_title(f'Particle Swarm Optimization - 1D (Iteration {i})')
        
        # Draw movement trajectories if not the first frame
        if i > 0:
            for j, (prev_pos, curr_pos) in enumerate(zip(position_history[i-1], positions)):
                prev_fitness = -objective_function_1d(prev_pos)
                curr_fitness = fitness_values[j]
                arrow = ax.arrow(prev_pos, prev_fitness, 
                          curr_pos - prev_pos, curr_fitness - prev_fitness,
                          head_width=2, head_length=1, fc='gray', ec='gray', alpha=0.3,
                          length_includes_head=True)
                arrows.append(arrow)
        
        # Update slider position without triggering callback
        slider.set_val(i)
        
        return particles_scatter, personal_best_scatter, global_best_scatter
    
    # Create slider for manual frame selection
    ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(ax_slider, 'Iteration', 0, len(position_history) - 1, valinit=0, valstep=1)
    
    # Flag to prevent recursive calls
    is_updating = False
    
    # Create animation with slower interval for better visibility
    ani = animation.FuncAnimation(
        fig, animate, frames=len(position_history),
        interval=500, blit=False, repeat=True
    )
    
    # Play/pause functionality
    is_playing = [False]  # Use a list to make it mutable
    
    # Update function for manual navigation
    def update_slider(val):
        nonlocal is_updating
        if is_updating:
            return
            
        is_updating = True
        i = int(slider.val)
        
        # Stop animation when using slider
        ani.event_source.stop()
        is_playing[0] = False
        play_button.label.set_text('Play')
        
        # Directly call animate with current frame
        animate(i)
        fig.canvas.draw_idle()
        is_updating = False
    
    slider.on_changed(update_slider)
    
    # Initially pause the animation
    ani.event_source.stop()
    
    # Create play/pause button
    ax_button = plt.axes([0.1, 0.1, 0.1, 0.03])
    play_button = Button(ax_button, 'Play/Pause')
    
    def toggle_play(event):
        is_playing[0] = not is_playing[0]
        if is_playing[0]:
            ani.event_source.start()
            play_button.label.set_text('Pause')
        else:
            ani.event_source.stop()
            play_button.label.set_text('Play')
        fig.canvas.draw_idle()
    
    play_button.on_clicked(toggle_play)
    
    # Show the plot
    # Removed tight_layout() to avoid warning
    plt.show()
    
    return ani

if __name__ == "__main__":
    visualize_pso()
