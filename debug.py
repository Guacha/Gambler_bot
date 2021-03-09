HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
    
def module_message(message, module_name, level=None, *modifiers):
    valid_levels = {
        "warning": WARNING,
        "error": FAIL,
        "message": OKCYAN,
        "ok": OKGREEN,
        "":""
    }
    valid_mods = {
        "bold": BOLD,
        "underline": UNDERLINE,
        "header": HEADER    
    }
    mods = "".join([valid_mods[mod] for mod in modifiers]) if modifiers else ""
    level_str = valid_levels[level] if level else ""
    
    print(f"{mods}{level_str}[{module_name}] {level.capitalize() if level else 'Info'}: {message}{ENDC}")
    
# Sobrecarga de métodos para el bot, todos funcionan exactamente igual    
def bot_print(message, *modifiers):
    module_message(message, "GamBlot", None, *modifiers)

def bot_warning(message, *modifiers):
    module_message(message, "GamBlot", "warning", *modifiers)
    
def bot_success(message, *modifiers):
    module_message(message, "GamBlot", "ok", *modifiers)
    
def bot_error(message, *modifiers):
    module_message(message, "GamBlot", "error", *modifiers)
    
def bot_message(message, *modifiers):
    module_message(message, "GamBlot", "message", *modifiers)
    
    
# Sobrecarga de métodos para módulos, todos funcionan exactamente igual
def mod_print(message, name, *modifiers):
    module_message(message, name, "", *modifiers)

def mod_warning(message, name, *modifiers):
    module_message(message, name, "warning", *modifiers)
    
def mod_success(message, name, *modifiers):
    module_message(message, name, "ok", *modifiers)
    
def mod_error(message, name, *modifiers):
    module_message(message, name, "error", *modifiers)
    
def mod_message(message, name, *modifiers):
    module_message(message, name, "message", *modifiers)
    