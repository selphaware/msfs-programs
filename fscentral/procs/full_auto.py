from aircraft.aircraft_class import Aircraft
from fscentral.procs.airproc import AirProc
from auxiliary.structs import PROC_INPUT_STRUCT
from fscentral.procs.approach_land import ApproachLandProc
from fscentral.procs.procs_inputs import TAKEOFF_INPUTS, APPROACH_LAND_INPUTS
from fscentral.procs.takeoff import TakeOffProc

from colorama import Fore, Style, Back
from time import sleep


class FullAutoProc(AirProc):
    def __init__(self, airplane: Aircraft, inputs: PROC_INPUT_STRUCT):
        super().__init__(airplane, inputs)
        self.__name = "FULL_AUTO"
        self.takeoff_proc = TakeOffProc(airplane, TAKEOFF_INPUTS)
        self.appla_proc = ApproachLandProc(airplane, APPROACH_LAND_INPUTS)

    def exproc(self, **inputs):
        # get input values (and defaults)
        inputs = self.get_inputs(inputs)
        com = self.com

        inp = input(Fore.WHITE + Back.GREEN + "Do you wish to proceed with "
                                              "automatic takeoff and landing ? ["
                                              "Y|N] " + Style.RESET_ALL).upper()
        if not (inp == "Y"):
            print(Style.RESET_ALL + "Aborting.")
            return

        print(Style.RESET_ALL + "Proceeding.")
        power = inputs["POWER"]
        rise_alt = inputs["RISE_ALT"]
        cruise_alt = inputs["CRUISE_ALT"]
        cruise_kspd = inputs["CRUISE_KSPD"]
        steady_throttle = inputs["POWER"]
        elevator_trim = inputs["ELEVATOR_TRIM"]
        liftoff_kspd = inputs["LIFTOFF_KSPD"]
        self.takeoff_proc.exproc(power=power, rise_alt=rise_alt,
                                 cruise_alt=cruise_alt, cruise_kspd=cruise_kspd,
                                 steady_throttle=steady_throttle,
                                 elevator_trim=elevator_trim,
                                 liftoff_kspd=liftoff_kspd)

        wp_id = inputs["RENDE_WP_ID"]
        print(Fore.LIGHTMAGENTA_EX + Back.LIGHTYELLOW_EX + f"Navigating at "
                                                           "cruise altitude "
                                                           "until we arrive "
                                                           f"at {wp_id}, "
              f"then we will proceed to approach and land at the destination "
              f"airport" + Style.RESET_ALL)

        wp_id = wp_id.upper()
        count = 0
        prev_ids = []
        approaching_rendezvous = False

        while wp_id not in prev_ids:
            next_id = com("G WP NX ID W").decode('utf-8')

            # set speed and altitude if reaching rendezvous wp
            if (wp_id == next_id) and not approaching_rendezvous:
                half_alt = min(com("G ALT W"), 8000 + round(com("G GD ALT W")))
                print(Fore.CYAN + f"@ RENDEZVOUS Reducing Altitude to"
                                  f" {half_alt}" +
                      Style.RESET_ALL)
                com(f"S ALT -> {half_alt} / 3.5")

                print(Fore.CYAN +
                      f"Next WP is RENDEZVOUS point {next_id}. Reducing to "
                      f"200KTS" +
                      Style.RESET_ALL)
                com("S SPD K -> 200 / 2")

                approaching_rendezvous = True

            # control to ensure altitude is high enough i.e. don't crash into
            # mountains
            # good test is to fly to OPIS (Pakistan) via Afghanistan BOBAM wp.
            chk_pln_alt = com("G ALT W")
            chk_grd_alt = com("G GD ALT W")
            if (chk_pln_alt - chk_grd_alt) < 2500:
                fix_alt = round(chk_grd_alt) + 3000
                print(Fore.LIGHTWHITE_EX + Back.RED +
                      f" Altitude TOO LOW @ {chk_pln_alt} < 2500ft above ground level. "
                      f"Ascending to FIX altitude of {fix_alt}." + Style.RESET_ALL)
                com(f"S ALT -> {fix_alt} / 0.1")

            # prev wp id cache
            prev_id = com("G WP PRE ID W").decode('utf-8')
            if prev_id not in prev_ids:
                prev_ids.append(prev_id)
            sleep(1)

            # pinfo every 5 mins
            if count % (60 * 5) == 0:
                patt = "-" * 55
                print(Fore.GREEN + patt + Style.RESET_ALL)
                self.airplane.pinfo()
                print("PREV_WPS: ", prev_ids)
            count += 1

        print("\n" + Fore.RED + Back.WHITE + f"Reached {wp_id}." +
              Style.RESET_ALL)

        runway = inputs["RUNWAY"]
        land_alt = inputs["LAND_ALT"]
        floating_alt = inputs["FLOATING_ALT"]
        cut_off = inputs["CUT_OFF"]
        self.appla_proc.exproc(runway=runway, land_alt=land_alt,
                               floating_alt=floating_alt, cut_off=cut_off)
