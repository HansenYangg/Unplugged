import PyInstaller.__main__
import os
import shutil
from os import path
import llama_cpp


#exact same as 1b except for name of distributable and the model included

def create_package():
    "create the distributable package for 1B model"
    dist_dir = "dist_llama-1b"
    if path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    print("Creating package for llama-1b...")

    llama_cpp_path = os.path.dirname(llama_cpp.__file__)
    llama_lib_path = os.path.join(os.path.dirname(llama_cpp.__file__), "lib", "libllama.dylib")

    PyInstaller.__main__.run([
        'main.py',
        '--name=llm_server_llama-1b',
        '--clean',
        '--distpath=dist_llama-1b',
        '--add-data=models/llama-1b-q4.gguf:models',  
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
        '--onefile'
        
    ])

    
    os.makedirs(path.join(dist_dir, 'models'), exist_ok=True)
    shutil.copy('models/llama-1b-q4.gguf', path.join(dist_dir, 'models/llama-1b-q4.gguf'))

    create_run_scripts(dist_dir)
    print("Packaging complete for llama-1b! Located in the 'dist_llama-1b' directory.")



def create_run_scripts(dist_dir):
 
    windows_script = """
    @echo off
    echo Starting LLM Server...
  
    start /B llm_server_llama-1b.exe

    echo Server started! Access will be available at http://localhost:8000
    echo Press Ctrl+C to stop the server
    pause
    """.strip()
    
   
    unix_script = """
    #!/bin/bash
    echo "Starting LLM Server..."

    chmod +x ./llm_server_llama-1b
    ./llm_server_llama-1b &

    echo "Server started! Access will be available at http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    read -p "Press Enter to exit..."
    pkill -f llm_server_llama-1b
    """.strip()

   
    with open(path.join(dist_dir, "run_server.bat"), "w") as f:
        f.write(windows_script)
    with open(path.join(dist_dir, "run_server.sh"), "w") as f:
        f.write(unix_script)
    os.chmod(path.join(dist_dir, "run_server.sh"), 0o755)

  



if __name__ == "__main__":
    print("Starting packaging process...")
    create_package()
