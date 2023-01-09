from typing import Dict, Optional
from simcoms import VarCom, EventCom, MAX_VAL
from simcentral import SimCentral
from colorama import Fore, Back, Style


class SimProcs(object):
    def __init__(self, sc: SimCentral):
        self.sc = sc

    def takeoff(self,
                power: int = -1,
                rise_alt: int = 2000,
                cruise_alt: int = 33000,
                cruise_kspd: int = 420,
                steady_throttle: bool = True
                ) -> Optional[Dict[str, str]]:

        print("Setting initial altitude")
        self.sc.execute("S ALT " +
                        (self.sc.get(VarCom.GROUND_ALTITUDE) + 10000),
                        "LO")

        print("Parking brakes OFF")
        self.sc.execute("PB", "LO")

        print("Engines/Throttle UP...")
        if power < 0:
            if not steady_throttle:
                self.sc.execute("TF", "LO")
            else:
                for i in range(10, 110, 10):
                    self.sc.execute(f"S T {i}", "LO")
                self.sc.execute("TF", "LO")
        else:
            if power > 100:
                print(Fore.RED + "ERROR: Power cannot be > 100%")
                return
            self.sc.execute(f"TS {round(power * MAX_VAL / 100)}", "LO")

        print("Lifting off...")
        rise_alt += self.sc.get(VarCom.GROUND_ALTITUDE)
        current_alt = 0
        wheel_down = True

        while current_alt < rise_alt:
            current_alt = self.sc.get(VarCom.PLANE_ALTITUDE)

            if (current_alt > 500 + self.sc.get(VarCom.GROUND_ALTITUDE)) and \
                    wheel_down:

                print("Reached 500 ft")
                print("Wheel gears UP")
                self.sc.execute("GU", "LO")
                wheel_down = False

                print("Flaps fully down")
                self.sc.execute("S FLAP 0", "LO")

                print("Set engines to 80%")
                self.sc.execute("S T 80", "LO")

        print("Turn Autopilot ON")
        self.sc.execute("AP ON", "HI")

        print("Turn TOGA/Autothrottle ON")
        self.sc.execute("TOGA", "HI")

        print("Turn LNAV Navigation ON")
        self.sc.execute("LNAV ON", "HI")

        print(f"Set cruise altitude of {cruise_alt} ft and speed {cruise_kspd} kts")
        self.sc.execute(f"S ALT {cruise_alt}", "LO")
        self.sc.execute(f"S SPD K {cruise_kspd}", "LO")

        print("Take off complete.")
        print("Hopefully you would have taken off safely and are soon ascending to your cruise "
              "altitude after which you should be heading towards your desitnation.")
