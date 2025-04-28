from pythonfmu import Fmi2Slave, Real, Fmi2Causality

class Cart(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mass = 1.0  # kg (M)
        self.m_pendulum = 0.1  # kg (m)
        self.position = 0.0
        self.velocity = 0.0
        self.force = 0.0
        self.Fpendulum = 0.0  # Input fra Pendulum

        self.register_variable(Real("mass", causality=Fmi2Causality.parameter))
        self.register_variable(Real("position", causality=Fmi2Causality.output))
        self.register_variable(Real("velocity", causality=Fmi2Causality.output))
        self.register_variable(Real("force", causality=Fmi2Causality.input))
        self.register_variable(Real("Fpendulum", causality=Fmi2Causality.input))  # Ny input

    def do_step(self, t, dt):
        total_force = self.force + self.Fpendulum
        total_mass = self.mass + self.m_pendulum  # M + m
        acc = total_force / total_mass  # Riktig akselerasjon (ligning 2)
        self.velocity += acc * dt
        self.position += self.velocity * dt
        return True