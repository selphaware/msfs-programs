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

        print(Fore.YELLOW + "Setting initial altitude")
        self.sc.execute("S ALT " +
                        (self.sc.get(VarCom.GROUND_ALTITUDE) + 10000),
                        "LO")

        print(Fore.CYAN + "Parking brakes OFF")
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

        print(Fore.LIGHTGREEN_EX + "Lifting off...")
        rise_alt += self.sc.get(VarCom.GROUND_ALTITUDE, wait=True)
        current_alt = 0
        wheel_down = True

        while current_alt < rise_alt:
            current_alt = self.sc.get(VarCom.PLANE_ALTITUDE, wait=True)

            if (current_alt > 500 + self.sc.get(VarCom.GROUND_ALTITUDE,
                                                wait=True)) and wheel_down:

                print(Fore.LIGHTBLUE_EX + "Reached 500 ft")
                print(Fore.LIGHTBLUE_EX + "Wheel gears UP")
                self.sc.execute("GR UP", "LO")
                wheel_down = False

                print(Fore.LIGHTBLUE_EX + "Flaps fully down")
                self.sc.execute("S FLAP 0", "LO")

                print(Fore.LIGHTBLUE_EX + "Set engines to 80%")
                self.sc.execute("S T 80", "LO")

        print(Fore.LIGHTMAGENTA_EX + "Turn Autopilot ON")
        self.sc.execute("AP ON", "HI")

        print(Fore.LIGHTMAGENTA_EX + "Turn TOGA/Autothrottle ON")
        self.sc.execute("TOGA", "HI")

        print(Fore.LIGHTMAGENTA_EX + "Turn LNAV Navigation ON")
        self.sc.execute("LNAV ON", "HI")

        print(Fore.YELLOW + f"Set cruise altitude of {cruise_alt} ft and speed {cruise_kspd} kts")
        self.sc.execute(f"S ALT {cruise_alt}", "LO")
        self.sc.execute(f"S SPD K {cruise_kspd}", "LO")

        print(Fore.WHITE + "Take off complete.")
        print("Hopefully you would have taken off safely and are soon ascending to your cruise "
              "altitude after which you should be heading towards your "
              "desitnation." + Style.RESET_ALL)

    def approach_land(self,
                      runway: str, land_alt: int,
                      floating_alt: int = 1500) -> None:
        print(Fore.LIGHTGREEN_EX + "Ensure AutoPilot is ON")
        self.sc.execute("AP ON", "HI")

        print("Ensure LNAV is ON")
        self.sc.execute("LNAV ON", "HI")

        print("Bring speed down to 200 knots")
        cspeed = 200
        self.sc.execute(f"S SPD K {cspeed}", "LO")

        print("Come to above 6000 ft above ground level")
        new_g_alt = round(6000 + max(land_alt,
                                     self.sc.get(VarCom.GROUND_ALTITUDE, wait=True)))
        self.sc.execute(f"S ALT "
                        f"{new_g_alt}", "LO")

        print("Set Auto brakes to MAX")
        self.sc.execute("ABR M", "MI")

        # keep decreasing alt + speed, increase flaps until approaching airport
        print(Fore.LIGHTMAGENTA_EX + "Descend, decrease speed, increase flaps " \
                                   "iteratively")
        next_wp_id = "RANDOM_QWERT"
        prev_id = next_wp_id

        while not (bytes(f"RW{runway}", 'utf-8') == next_wp_id[0:(len(runway) + 2)]):

            next_wp_id = self.sc.get(VarCom.GPS_WP_NEXT_ID, wait=True)

            if not (next_wp_id == prev_id):

                print(Fore.LIGHTYELLOW_EX + Back.BLUE + "Getting next ALT...")
                new_alt, max_alt = self.sc.get_next_alt()

                n_alt = max(
                    floating_alt + max(land_alt,
                                       self.sc.get(VarCom.GROUND_ALTITUDE,
                                                   wait=True)),
                    min(max_alt, new_alt)
                    )

                self.sc.execute(f"S ALT {n_alt}", "LO")

                self.sc.execute("S FLAP I", "LOW")

                cspeed -= 5
                cspeed = max(165, cspeed)
                self.sc.execute(f"S SPD K {cspeed}", "LO")

                prev_id = next_wp_id
                print(Fore.LIGHTWHITE_EX + Back.MAGENTA +
                    f"AT {next_wp_id}, DECREASING ALT to {n_alt}, SPEED to "
                    f"{cspeed}"
                    )

        print(Style.RESET_ALL + Fore.LIGHTBLUE_EX + "APPROACHING AIRPORT !!!")

        # reduce speed to 165 knots
        print(Fore.LIGHTYELLOW_EX + "Reduce speed to 165 knoits")
        self.sc.execute("S SPD K 165", "LO")

        # full flaps
        print("Flaps fully up")
        self.sc.execute("S FLAP 100", "LO")

        # enable approach model to automatically descend/approach airport and land
        print("Enable APR approach mode")
        self.sc.execute("APR ON", "HI")

        # wheel gear down
        print("Wheel Gears down")
        self.sc.execute("GR DO", "LO")

        # while descending and landing, ensure speed and alt are correct
        print("Descending at 155 knots until gears are on the ground")
        while (self.sc.get(VarCom.PLANE_ALTITUDE) / land_alt) - 1 > 0.055:
            self.sc.execute("S SPD K 155", "LO")
            self.sc.execute("APR ON", "LO")

        print(Fore.CYAN + "WE ARE ON THE GROUND !")

        # turn off auto throttle
        print("Turn Autothrottle off")
        self.sc.execute("AT", "LO")

        # cut engines
        print("Cut the engines off, autobrakes should be applied")
        self.sc.execute("T C", "LO")

        print(Style.RESET_ALL + "Hopefully we have landed safely in the right "
                                "place!")
