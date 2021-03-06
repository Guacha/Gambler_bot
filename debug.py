HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
    
def module_message(message, module_name, level="message", *modifiers):
    valid_levels = {"warning": WARNING,
                    "error": FAIL,
                    "message": "",
                    "important": BOLD,
                    "ok", OKGREEN,
                    "":}
    print(f"{valid_levels[level] if level in valid_levels else ''}\
          [{module_name}][{level.upper()}]{message}{ENDC if level in valid_levels else ''}")
    
def bot_message(message, level):
    module_message(message, level, "GamBlot")
    