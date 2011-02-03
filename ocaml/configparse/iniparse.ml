(* An ocaml Library which parses a collection of config files *)

let lines_to_dict lines = "pass" in

class iniparser (config_init) =
  object (self)
    val config = config_init

    method get_config = config

    method get_lines =

end;;
