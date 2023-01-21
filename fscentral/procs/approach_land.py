from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT

from colorama import Fore, Style, Back


class ApproachLandProc(AirProc):
    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        super().__init__(airplane, inputs)
        self.__name = "APPROACH_LAND"

    def exproc(self, **inputs):
        """

        :param inputs:
        :return:
        """
        # get input values (and defaults)
        inputs = self.get_inputs(inputs)
        com = self.com

        print("\nProceeding with Approach & Landing.")
        print(Fore.LIGHTGREEN_EX + "Ensure AutoPilot is ON")
        com("AP ON / 3.5")

        print("Ensure LNAV is ON")
        com("LNAV ON / 3.5")

        print("Come to above 6000 ft above ground level")
        land_alt = inputs["LAND_ALT"]
        new_g_alt = round(6000 + max(land_alt, com("G GD ALT W")))
        com(f"S ALT -> {new_g_alt} / 0.1")

        print("Bring speed down to 200 knots")
        cspeed = 200
        com(f"S SPD K -> {cspeed} / 0.1")

        print("Set Auto brakes to MAX")
        self.set_max_autobrake()

        # keep decreasing alt + speed, increase flaps until approaching airport
        print(
            Fore.LIGHTMAGENTA_EX +
            "Descend, decrease speed, increase flaps iteratively"
        )
        next_wp_id = "RANDOM_QWERT"
        prev_id = next_wp_id
        runway = inputs["RUNWAY"]
        floating_alt = inputs["FLOATING_ALT"]

        while not (bytes(f"RW{runway}", 'utf-8') == next_wp_id[0:(len(runway) + 2)]):

            next_wp_id = com("G WP NX ID W")

            if not (next_wp_id == prev_id):
                print(Fore.LIGHTYELLOW_EX + Back.BLUE + "Getting next ALT...")
                new_alt = min(
                    self.get_next_alt(floating_alt, land_alt),
                    new_g_alt
                )

                com(f"S ALT -> {new_alt} / 0.1")

                com("S FLAP I / 0.1")

                cspeed -= 5
                cspeed = max(165, cspeed)
                com(f"S SPD K -> {cspeed} / 0.1")

                prev_id = next_wp_id
                print(
                    Fore.LIGHTWHITE_EX + Back.MAGENTA +
                    f"AT {next_wp_id}, DECREASING ALT to {new_alt}, SPEED to "
                    f"{cspeed}"
                    )

        print(Style.RESET_ALL + Fore.LIGHTBLUE_EX + "APPROACHING AIRPORT !!!")

        final_alt = min(int(land_alt + floating_alt), com("G ALT W"))
        print(Fore.LIGHTCYAN_EX + f"Reducing altitude to {final_alt}")
        com(f"S ALT -> {final_alt} / 2")

        # reduce speed to 165 knots
        print(Fore.LIGHTYELLOW_EX + "Reduce speed to 165 knoits")
        com("S SPD K -> 165 / 2")

        # full flaps
        print("Flaps fully up")
        com("S FLAP -> 30 / 2")

        # enable approach model to automatically descend/approach airport and land
        print("Enable APR approach mode")
        com("APR ON / 3.5")

        # wheel gear down
        print("Wheel Gears down")
        while com("G GR POS W") == 0:
            # 0 - UP,
            # 1 - DOWN
            com("GR DO / 2")

        # while descending and landing, ensure speed and alt are correct
        cut_off = inputs["CUT_OFF"]
        print("Descending at 155 knots until gears are on the ground")
        while (com("G ALT W") / land_alt) - 1 > cut_off / 100:
            com("S SPD K -> 155 / 0.1")
            com("APR ON / 0.1")

        print(Fore.CYAN + "WE ARE ON THE GROUND !")

        # turn off auto throttle
        print("Turn Autothrottle off")
        com("AT / 2")

        # cut engines
        print("Cut the engines off, autobrakes should be applied")
        com("T C / 0.1")

        print(Style.RESET_ALL + "Hopefully we have landed safely in the right place!")
