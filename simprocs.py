from typing import Dict, Optional, Tuple, Any, List
from simcoms import MAX_VAL
from simcentral import SimCentral
from colorama import Fore, Back, Style
import time


class SimProcs(object):
    def __init__(self, sc: SimCentral):
        self.sc = sc

    def takeoff(self,
                power: int = -1,
                rise_alt: int = 2000,
                cruise_alt: int = 33000,
                cruise_kspd: int = 420,
                steady_throttle: int = 1
                ) -> Optional[Dict[str, str]]:

        print("\nProceeding with Takeoff.")
        print(Fore.YELLOW + "Setting initial altitude")
        gr_alt = self.sc.get("GROUND_ALTITUDE", wait=True)
        self.sc.execute("S ALT " +
                        str(round(gr_alt + 10000)),
                        "LO")

        print(Fore.CYAN + "Parking brakes OFF")
        self.sc.execute("PB", "LO")

        print("Engines/Throttle UP...")
        if power < 0:
            if not (steady_throttle == 1):
                self.sc.execute("T F", "LO")
            else:
                for i in range(10, 110, 10):
                    self.sc.execute(f"S T {i}", "LO")
                self.sc.execute("T F", "LO")
        else:
            if power > 100:
                print(Fore.RED + "ERROR: Power cannot be > 100%")
                return
            self.sc.execute(f"S T {round(power * MAX_VAL / 100)}", "LO")

        print(Fore.LIGHTGREEN_EX + "Lifting off...")
        rise_alt += self.sc.get("GROUND_ALTITUDE", wait=True)
        current_alt = 0
        wheel_down = True

        while current_alt < rise_alt:
            current_alt = self.sc.get("PLANE_ALTITUDE", wait=True)

            if (current_alt > 500 + self.sc.get("GROUND_ALTITUDE",
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
                      floating_alt: int = 1500,
                      cut_off: float = 5.5) -> None:
        print("\nProceeding with Approach & Landing.")
        print(Fore.LIGHTGREEN_EX + "Ensure AutoPilot is ON")
        self.sc.execute("AP ON", "HI")

        print("Ensure LNAV is ON")
        self.sc.execute("LNAV ON", "HI")

        print("Bring speed down to 200 knots")
        cspeed = 200
        self.sc.execute(f"S SPD K {cspeed}", "LO")

        print("Come to above 6000 ft above ground level")
        new_g_alt = round(6000 + max(land_alt,
                                     self.sc.get("GROUND_ALTITUDE", wait=True)))
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

            next_wp_id = self.sc.get("GPS_WP_NEXT_ID", wait=True)

            if not (next_wp_id == prev_id):

                print(Fore.LIGHTYELLOW_EX + Back.BLUE + "Getting next ALT...")
                new_alt, max_alt = self.sc.get_next_alt()

                n_alt = max(
                    floating_alt + max(land_alt,
                                       self.sc.get("GROUND_ALTITUDE",
                                                   wait=True)),
                    min(max_alt, new_alt)
                    )

                self.sc.execute(f"S ALT {n_alt}", "LO")

                self.sc.execute("S FLAP I", "LO")

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
        while (self.sc.get("PLANE_ALTITUDE") / land_alt) - 1 > cut_off / 100:
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

    def start_finish(
            self,
            runway: str,
            land_alt: int,
            wp_id: str,
            power: int = -1,
            rise_alt: int = 2000,
            cruise_alt: int = 33000,
            cruise_kspd: int = 420,
            steady_throttle: int = 1,
            floating_alt: int = 1500,
            cut_off: float = 5.5
    ) -> None:
        inp = input(Fore.WHITE + Back.GREEN + "Do you wish to proceed with "
                                              "automatic takeoff and landing ? ["
                                              "Y|N] " + Style.RESET_ALL).upper()
        if inp == "Y":
            print(Style.RESET_ALL + "Proceeding.")
            self.takeoff(power, rise_alt, cruise_alt, cruise_kspd, steady_throttle)

            print(Fore.LIGHTMAGENTA_EX + Back.LIGHTYELLOW_EX + f"Navigating at "
                                                               "cruise altitude "
                                                               "until we arrive "
                                                               f"at {wp_id}, "
                  f"then we will proceed to approach and land at the destination "
                  f"airport" + Style.RESET_ALL)
            wp_id = wp_id.upper()
            count = 0
            prev_ids = []
            while wp_id not in prev_ids:
                prev_id = self.sc.get("GPS_WP_PREV_ID", wait=True).decode('utf-8')
                if prev_id not in prev_ids:
                    prev_ids.append(prev_id)
                time.sleep(1)
                if count % (60 * 5) == 0:
                    patt = "-" * 55
                    print(Fore.GREEN + patt + Style.RESET_ALL)
                    self.sc.pinfo()
                    print("PREV_WPS: ", prev_ids)
                count += 1

            print("\n" + Fore.RED + Back.WHITE + f"Reached f{wp_id}." +
                  Style.RESET_ALL)

            self.approach_land(runway, land_alt, floating_alt, cut_off)
        else:
            print(Style.RESET_ALL + "Aborting.")

    def autobrakes_max(self):
        for _ in range(6):
            self.sc.execute("ABR I", "LO")

    @staticmethod
    def get_proc_inputs(
            proc_args: List[Any],
            proc_map: List[Tuple[str, Any, Any]]) -> List[Any]:

        if len(proc_args) > 1:
            proc_args = [proc_map[i][2](x)
                         for i, x in enumerate(proc_args[1:])]

        else:
            proc_args = []
            for proc_var, proc_def, proc_type in proc_map:
                proc_in = input(
                    Back.YELLOW + Fore.BLACK +
                    f"Input: {proc_var} = [ {proc_def} ] >> ")
                val = proc_type(proc_in) if len(proc_in) else proc_def
                proc_args.append(val)

        return proc_args

    def inter(self) -> None:
        inp = ""
        print(
            "\n" + Fore.BLACK + Back.LIGHTCYAN_EX +
            " ***** --- ** - Flight Simulator "
            "COMMAND CONSOLE - ** --- ***** " +
            Fore.LIGHTRED_EX + Back.BLACK +
            " by Usman Ahmad @ selphaware @ polardesert\n" +
            Style.RESET_ALL
            )

        while not (inp.upper() == "Q"):
            inp = input(Fore.LIGHTBLUE_EX + "< FS-COM > :: >> " + Fore.LIGHTRED_EX)
            inp = inp.upper()

            if not (inp == "Q"):

                if inp == "P":
                    self.sc.pinfo()

                elif inp[0:4] == "TKOF":
                    tk_args = inp.split(chr(32))
                    tk_map = [
                        ("POWER", -1, int),
                        ("RISE_ALT", 2000, int),
                        ("CRUISE_ALT", 33000, int),
                        ("CRUISE_KSPD", 420, int),
                        ("STEADY_THROTTLE", 1, int)
                    ]
                    tk_args = self.get_proc_inputs(tk_args, tk_map)
                    print(Style.RESET_ALL + "Starting TAKEOFF")
                    self.takeoff(*tk_args)

                elif inp[0:4] == "APLA":
                    ap_args = inp.split(chr(32))
                    ap_map = [
                        ("RUNWAY", None, str),
                        ("LAND_ALT", None, int),
                        ("FLOATING_ALT", 1500, int),
                        ("CUT_OFF", 5.5, float)
                    ]
                    ap_args = self.get_proc_inputs(ap_args, ap_map)
                    print(Style.RESET_ALL + "Starting APPROACH & LAND")
                    self.approach_land(*ap_args)

                elif inp[0:4] == "STFI":
                    stfi_args = inp.split(chr(32))
                    stfi_map = [
                        ("RUNWAY", None, str),
                        ("LAND_ALT", None, int),
                        ("WP_ID", None, str),
                        ("POWER", -1, int),
                        ("RISE_ALT", 2000, int),
                        ("CRUISE_ALT", 33000, int),
                        ("CRUISE_KSPD", 420, int),
                        ("STEADY_THROTTLE", 1, int),
                        ("FLOATING_ALT", 1500, int),
                        ("CUT_OFF", 5.5, float)
                    ]
                    stfi_args = self.get_proc_inputs(stfi_args, stfi_map)
                    print(Style.RESET_ALL +
                          f"Starting TAKEOFF, RENDEVOUS WITH {stfi_args[2]}, "
                          f"APPROACH & LAND on RUNWAY {stfi_args[0]}, "
                          f"and LANDING ALT {stfi_args[1]}")

                    self.start_finish(*stfi_args)

                else:
                    print(self.sc.execute(inp, "LO"))

            else:
                print(Style.RESET_ALL + "Quitting FS-COM.")
