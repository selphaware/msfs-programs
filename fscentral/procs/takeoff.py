from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT
from auxiliary.conversions import MAX_VAL, M_TO_FT

from colorama import Fore, Style, Back


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

        com = self.airplane.com_inter

        print("\nProceeding with Takeoff.")
        print(Fore.YELLOW + "Setting initial altitude to ")
        gr_alt = com("G GD ALT / 0.1 W") + 10000  # TODO: DO I NEED TO APPLY CAST_LOGIC?
        com(f"S ALT -> {gr_alt} / 0.1")
        print(Fore.YELLOW + f"Setting initial altitude to {gr_alt}")

        print(Fore.CYAN + "Parking brakes OFF")
        com("PB / 0.1")

        print("Engines/Throttle UP...")
        power: int = inputs["POWER"]
        steady_throttle: int = inputs["STEADY_THROTTLE"]
        if power < 0:
            if not (steady_throttle == 1):
                com("T F / 0.1")
            else:
                for i in range(10, 110, 10):
                    com(f"S T {i} / 0.1")
                com("T F / 0.1")
        else:
            if power > 100:
                print(Fore.RED + "ERROR: Power cannot be > 100%")
                return
            com(f"S T {round(power * MAX_VAL / 100)} / 0.1")

        print(Fore.LIGHTGREEN_EX + "Lifting off...")
        rise_alt = inputs["RISE_ALT"]
        liftoff_kspd = inputs["LIFTOFF_KSPD"]
        elevator_trim = inputs["ELEVATOR_TRIM"]
        rise_alt += com("G GD ALT W") * M_TO_FT
        current_alt = 0
        wheel_down = True
        elev_trim_set = False

        ttt = """
        while current_alt < rise_alt:
            current_alt = com("G ALT W")

            if not elev_trim_set and (com("G SPD I W") > liftoff_kspd):
                print(Fore.LIGHTRED_EX +
                      f"Setting elevator trim to {elevator_trim}% for liftoff" +
                      Style.RESET_ALL)
                com(f"S E T {elevator_trim}", time_sleep=0.1)
                elev_trim_set = True

            if (current_alt > 500 + self.sc.get("GROUND_ALTITUDE",
                                                wait=True) * M_TO_FT) and wheel_down:

                print(Fore.LIGHTBLUE_EX + "Reached 500 ft above ground level")
                print(Fore.LIGHTBLUE_EX + "Wheel gears UP")
                self.sc.execute("GR UP", "LO")
                wheel_down = False

                print(Fore.LIGHTBLUE_EX + "Flaps fully down")
                self.sc.execute("S FLAP 0", "LO")

                print(Fore.LIGHTBLUE_EX + "Set engines to 80%")
                self.sc.execute("S T 80", "LO")
        """