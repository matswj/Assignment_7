from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import math

class Pendulum(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.m = 0.1     # kg
        self.l = 1.0     # m
        self.g = 9.81    # m/s²

        self.theta = math.radians(20)  # initial 20 deg
        self.omega = 0.0               # initial angular velocity
        self.x_ddot = 0.0              # vognens aks
        self.Fpendulum = 0.0           # Ny variabel for kraft fra pendel

        self.register_variable(Real("theta", causality=Fmi2Causality.output))
        self.register_variable(Real("omega", causality=Fmi2Causality.output))
        self.register_variable(Real("x_ddot", causality=Fmi2Causality.input))  # fra Cart
        self.register_variable(Real("Fpendulum", causality=Fmi2Causality.output))  # Ny output

    def do_step(self, t, dt):
        # Beregn Fpendulum (ligning 5)
        torque_gravity = self.m * self.g * self.l * math.sin(self.theta)
        torque_cart = -self.m * self.l * self.x_ddot * math.cos(self.theta)
        torque_total = torque_gravity + torque_cart
        inertia = self.m * self.l ** 2
        alpha = torque_total / inertia  # vinkelakselerasjon

        # Beregn Fpendulum = ml(sin(theta)omega² - cos(theta)alpha)
        self.Fpendulum = self.m * self.l * (
            math.sin(self.theta) * self.omega**2 - 
            math.cos(self.theta) * alpha
        )

        # Oppdater omega og theta
        self.omega += alpha * dt
        self.theta += self.omega * dt
        return True