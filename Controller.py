from pythonfmu import Fmi2Slave, Real, Fmi2Causality

class Controller(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Regulatorparametere med defaultverdier
        self.k1 = -1.0
        self.k2 = -2.0
        self.k3 = -30.0
        self.k4 = -10.0

        # Input-signaler
        self.theta = 0.0
        self.omega = 0.0
        self.x = 0.0
        self.x_dot = 0.0

        # Output-signal
        self.force = 0.0

        # Registrer parametere slik at de kan settes utenfra (f.eks. i Ecos)
        self.register_variable(Real("k1", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k2", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k3", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k4", causality=Fmi2Causality.parameter))

        # Registrer inputs
        self.register_variable(Real("theta", causality=Fmi2Causality.input))
        self.register_variable(Real("omega", causality=Fmi2Causality.input))
        self.register_variable(Real("x", causality=Fmi2Causality.input))
        self.register_variable(Real("x_dot", causality=Fmi2Causality.input))

        # Registrer output
        self.register_variable(Real("force", causality=Fmi2Causality.output))

    def do_step(self, t, dt):
    # Bruk riktig fortegn: F = -k1θ -k2ω -k3x -k4x_dot
        self.force = -(
        self.k1 * self.theta +
        self.k2 * self.omega +
        self.k3 * self.x +
        self.k4 * self.x_dot
        )
        return True