from colorama import Fore, init
from .core.interfaces import SessionManager
from .messages.message import user_message
init(autoreset=True)

def cli(session: SessionManager):
    while True:
        thinking = False
        replying = False
        using_tool = False                                                
        user_input = input(Fore.GREEN + '\n>>> ')   
        try:                                                
            for a in session.handle_user_message(user_message(text=user_input)):
                if a.behavior == 'message':
                    continue
                behavior = a.behavior
                content = a.content
            
                if behavior == 'thinking':
                    if not thinking:
                        thinking = True
                        replying = False
                        using_tool = False
                        print (Fore.LIGHTRED_EX + '\nthinking> ', end="")
                    print (Fore.LIGHTRED_EX + content, end="")

                if behavior == 'replying':
                    if not replying:
                        thinking = False
                        replying = True
                        using_tool = False
                        print (Fore.CYAN + '\nagent> ', end="")
                    print (Fore.CYAN + content, end="")

                if behavior == 'tool_calls':
                    if not using_tool:
                        thinking = False
                        replying = False
                        using_tool = True
                        print (Fore.LIGHTYELLOW_EX + "\ntool> ", end="")
                    print (Fore.LIGHTYELLOW_EX + str(a.content))

                if behavior == 'done':
                    print (Fore.CYAN + f'\nagent turn ended: {content}')

        except KeyboardInterrupt:
            pass