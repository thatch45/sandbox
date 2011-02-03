class ini_config path_init =
    let orig_path = path_init in
    object (self)
        (* Set up module values *)
        val mutable path = orig_path

        method get_config_path = path
        method set_config new_path = path <- new_path
        
        
    end;;
        


