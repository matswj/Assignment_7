from ecospy import EcosSimulation, EcosSimulationStructure
from ecospy.plotter import Plotter, TimeSeriesConfig
import os

# Tving single-thread hvis nødvendig
os.environ["ECOSPYSIM_THREADS"] = "1"

if __name__ == "__main__":
    ss = EcosSimulationStructure()

    # Legg til FMU-modellene
    ss.add_model("cart", "Cart.fmu")
    ss.add_model("pendulum", "Pendulum.fmu")
    ss.add_model("controller", "Controller.fmu")

    # Koble komponenter
    ss.make_real_connection("controller::force", "cart::force")
    ss.make_real_connection("cart::position", "controller::x")
    ss.make_real_connection("cart::velocity", "controller::x_dot")
    ss.make_real_connection("cart::force", "pendulum::x_ddot")
    ss.make_real_connection("pendulum::Fpendulum", "cart::Fpendulum")
    ss.make_real_connection("pendulum::theta", "controller::theta")
    ss.make_real_connection("pendulum::omega", "controller::omega")

    # Initialverdier
    params = {
        "pendulum::theta": 20 * 3.1416 / 180,
        "pendulum::omega": 0.0,
        "cart::position": 0.0,
        "cart::velocity": 0.0,
        "cart::mass": 1.0,
        "controller::k1": -1.0,
        "controller::k2": -2.0,
        "controller::k3": -30.0,
        "controller::k4": -10.0
    }

    ss.add_parameter_set("initial", params)

    # Konfigurer plotting
    result_file = "results.csv"
    config = TimeSeriesConfig(
        title="Invertert pendel på vogn",
        y_label="Verdi",
        identifiers=["cart::position", "pendulum::theta"]
    )

    # Simulering med feilhåndtering
    try:
        with EcosSimulation(structure=ss, step_size=0.01) as sim:
            sim.add_csv_writer(result_file)
            sim.init(parameter_set="initial")
            print("Starter simulering...")
            sim.step_until(5)  # Test med 5 sekunder først
            sim.terminate()
            print("Simulering vellykket!")
    except Exception as e:
        print(f"Feil under simulering: {e}")
        exit(1)

    # Plot resultater
    plotter = Plotter(result_file, config)
    plotter.show()

    input("Trykk Enter for å avslutte...")