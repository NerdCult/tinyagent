#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

import shutil, os
from pathlib import Path

def copy_built_in_tools(target_dir: str = f'{os.getcwd()}/tools'):
    ''' helper function to copy the built-in tools to the folder where you manage your own tools. '''
    src_path = Path(F'{os.path.dirname(__file__)}/../toolboxes/tools')
    dst_path = Path(target_dir)
    dst_path.mkdir(parents=True, exist_ok=True)
    
    for file in src_path.iterdir():
        if file.is_file() and not file.stem.startswith('__'):
            shutil.copy2(file, dst_path)

def copy_built_in_skills(target_dir: str = f'{os.getcwd()}/skills'):
    ''' helper function to copy the built-in skills to the folder where you manage your own skills. '''
    src_path = Path(F'{os.path.dirname(__file__)}/../skill_managers/skills')
    dst_path = Path(target_dir)
    dst_path.mkdir(parents=True, exist_ok=True)
    
    for file in src_path.iterdir():
        if file.is_file() and not file.stem.startswith('__'):
            shutil.copy2(file, dst_path)