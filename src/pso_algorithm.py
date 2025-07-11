import random
from src.particle import Particle

from src.test_functions import objective_function_1d


def main():
    # Example usage of the Particle class
    max_iterations = 50
    num_particles = 3
    w,c1,c2 = 0.8, 0.1, 0.1  # Inertia weight and acceleration coefficients

    particles_pool = [Particle(position=random.uniform(-10,10), velocity=0) for i in range(num_particles)]


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

    for iteration in range(max_iterations):
        for particle in particles_pool:
            # Simulate some logic to update particle's velocity and position
            new_velocity = w * particle.velocity + c1 * random.random()*(particle.best_position - particle.position) + c2 * random.random() * (swarm_best_position - particle.position)
            new_position = particle.position + new_velocity

            particle.update_velocity(new_velocity)
            particle.position = new_position

            particle.fitness = -objective_function_1d(particle.position)

            if particle.fitness > particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = particle.position
            
            if particle.fitness > swarm_best_fitness:
                swarm_best_fitness = particle.fitness
                swarm_best_position = particle.position
        
            # print(particle)
        print(f"Iteration {iteration + 1}/{max_iterations} completed.")
        print(f"Swarm best fitness: {swarm_best_fitness} at position {swarm_best_position}")
    





