

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fitness = float('-inf')
        self.best_fitness = float('-inf')
        self.best_position = position
    
    def update_velocity(self, new_velocity):
        self.velocity = new_velocity

    def __repr__(self):
        return f"Particle(position={self.position}, velocity={self.velocity}," \
               f"Best Position: {self.best_position}, Best Fitness: {self.best_fitness})"