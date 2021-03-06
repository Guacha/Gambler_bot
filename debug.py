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
    mods = " ".join([valid_mods[mod] for mod in modifiers[0]]) if modifiers else ""
    level = valid_levels[level] if level else ""
    
    print(f"{mods}{level}{message}{ENDC}")
    
    
def bot_message(message, level, *modifiers):
    module_message(message, "GamBlot", level, modifiers)
    