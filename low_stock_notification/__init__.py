from . import models

def uninstall_hook(env):  
   technical_name = __name__.split('.')[2] 
   env['res.config.settings'].clear_config_parameter(technical_name)
