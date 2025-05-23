import PyInstaller.__main__
import os
import shutil
from os import path
import llama_cpp

def create_package():
    "create the distributable package for 3B model"
    dist_dir = "dist_llama-3b"
    if path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    print("Creating the package for llama-3b...")

    llama_cpp_path = os.path.dirname(llama_cpp.__file__)
    llama_lib_path = os.path.join(os.path.dirname(llama_cpp.__file__), "lib", "libllama.dylib")


    # packages entire application (all files, dependencies, model, etc.)
    PyInstaller.__main__.run([
        'main.py',
        '--name=llm_server_llama-3b',
        '--clean',
        '--distpath=dist_llama-3b',
        '--add-data=models/llama-3b-q4.gguf:models',  
        '--add-data=config.py:.',
        '--add-data=wrapper.py:.',
        '--add-data=conversation.py:.',
        '--add-data=models.py:.',
        '--add-data=llms.py:.',
        f'--add-data={llama_cpp_path}:llama_cpp',
        f'--add-binary={llama_lib_path}:.',
        '--hidden-import=llama_cpp',
        '--hidden-import=fastapi',
        '--hidden-import=uvicorn',
        '--hidden-import=pydantic',
        '--hidden-import=collections',
        '--onefile' #creates a single executable; loads/starts the server when this file is ran (contains everything needed to run just in this executable alone)
    ])


    os.makedirs(path.join(dist_dir, 'models'), exist_ok=True)
    shutil.copy('models/llama-3b-q4.gguf', path.join(dist_dir, 'models/llama-3b-q4.gguf'))

    create_run_scripts(dist_dir)
    print("Packaging complete for llama-3b! Located in the 'dist_llama-3b' directory.")




def create_run_scripts(dist_dir):
    
    windows_script = """
    @echo off
    echo Starting LLM Server...
   

    start /B llm_server_llama-3b.exe
    
    echo Server started! Access will be available at http://localhost:8000
    echo Press Ctrl+C to stop the server
    pause
    """.strip()
    

    unix_script = """
    #!/bin/bash
    echo "Starting LLM Server..."

    chmod +x ./llm_server_llama-3b
    ./llm_server_llama-3b &

    echo "Server started! Access will be available at http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    read -p "Press Enter to exit..."
    pkill -f llm_server_llama-3b
    """.strip()

   
    with open(path.join(dist_dir, "run_server.bat"), "w") as f:
        f.write(windows_script)
    with open(path.join(dist_dir, "run_server.sh"), "w") as f:
        f.write(unix_script)
    os.chmod(path.join(dist_dir, "run_server.sh"), 0o755)




if __name__ == "__main__":
    print("Starting packaging process...")
    create_package()
