from .agent import Agent

def cli(agent: Agent):
    from colorama import Fore, init
    from .messages.message import user_message
    init(autoreset=True)
    while True:
        thinking = False
        replying = False
        using_tool = False                                                
        user_input = input(Fore.GREEN + '\n>>> ')   
        try:                                                
            for a in agent.chat(user_message(text=user_input)):
                behavior = a['behavior']
                content = a['content']
            
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

                if behavior == 'tool_call':
                    if not using_tool:
                        thinking = False
                        replying = False
                        using_tool = True
                        print (Fore.LIGHTYELLOW_EX + "\ntool> ", end="")
                    print (Fore.LIGHTYELLOW_EX + f"{a['tool'] or ""} > {content or "no content"}", end="")

                if behavior == 'done':
                    print (Fore.CYAN + f'\nagent turn ended: {content}')

        except KeyboardInterrupt:
            pass