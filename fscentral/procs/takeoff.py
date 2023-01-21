from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT

from colorama import Fore, Style


class TakeOffProc(AirProc):
    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        super().__init__(airplane, inputs)
        self.__name = "TAKEOFF"

    def exproc(self, **inputs):
        """

        :param inputs:
        :return:
        """
        # get input values (and defaults)
        inputs = self.get_inputs(inputs)
        com = self.com

        print("\nProceeding with Takeoff.")
        print(Fore.YELLOW + "Setting initial altitude to ")
        gr_alt = com("G GD ALT / 0.1 W") + 10000
        com(f"S ALT -> {gr_alt} / 0.1")
        print(Fore.YELLOW + f"Setting initial altitude to {gr_alt}")

        print(Fore.CYAN + "Parking brakes OFF")
        com("PB / 0.1")

        print("Engines/Throttle UP...")
        power: int = inputs["POWER"]
        steady_throttle: int = inputs["STEADY_THROTTLE"]
        if power < 0:
            if steady_throttle == 1:
                for i in range(10, 110, 10):
                    com(f"S T {i} / 0.2")

            com("T F / 0.1")
        else:
            if power > 100:
                print(Fore.RED + "ERROR: Power cannot be > 100%")
                return
            com(f"S T {power} / 0.1")

        print(Fore.LIGHTGREEN_EX + "Lifting off...")
        rise_alt = inputs["RISE_ALT"]
        liftoff_kspd = inputs["LIFTOFF_KSPD"]
        elevator_trim = inputs["ELEVATOR_TRIM"]
        rise_alt += com("G GD ALT W")
        current_alt = 0
        wheel_down = True
        elev_trim_set = False

        while current_alt < rise_alt:
            current_alt = com("G ALT W")

            if not elev_trim_set and (com("G SPD I W") > liftoff_kspd):
                print(Fore.LIGHTRED_EX +
                      f"Setting elevator trim to {elevator_trim}% for liftoff" +
                      Style.RESET_ALL)
                com(f"S E T {elevator_trim} / 0.1")
                elev_trim_set = True

            if (current_alt > 500 + com("G ALT W")) and wheel_down:

                print(Fore.LIGHTBLUE_EX + "Reached 500 ft above ground level")
                print(Fore.LIGHTBLUE_EX + "Wheel gears UP")
                com("GR UP / 0.1")
                wheel_down = False

                print(Fore.LIGHTBLUE_EX + "Flaps fully down")
                com("S FLAP 0 / 0.1")

                print(Fore.LIGHTBLUE_EX + "Set engines to 80%")
                com("S T 80 / 0.1")

        print(Fore.LIGHTMAGENTA_EX + "Turn Autopilot ON")
        com("AP ON / 3.5")

        print(Fore.LIGHTMAGENTA_EX + "Turn TOGA/Autothrottle ON")
        com("TOGA / 3.5")

        print(Fore.LIGHTMAGENTA_EX + "Turn LNAV Navigation ON")
        com("LNAV ON / 3.5")

        cruise_alt = inputs["CRUISE_ALT"]
        cruise_kspd = inputs["CRUISE_KSPD"]
        print(Fore.YELLOW + f"Set cruise altitude of {cruise_alt} ft and "
                            f"speed {cruise_kspd} kts")
        com(f"S ALT {cruise_alt} / 0.1")
        com(f"S SPD K {cruise_kspd} / 0.1")

        print(Fore.WHITE + "Take off complete.")
        print("Hopefully you would have taken off safely "
              "and are soon ascending to your cruise "
              "altitude after which you should be heading towards your "
              "desitnation." + Style.RESET_ALL)
