Are YOU a college student and your internet in the dorm is out but you need to finish an assignment and need an LLM for assistance?

Fear not.

HOW TO USE:

1. Make a directory for it
mkdir test_unplugged && cd test_unplugged

2. Clone repo and cd into it
git clone https://github.com/HansenYangg/Unplugged.git
cd Unplugged

3. Install dependencies (strongly recommended Python 3.11, may not work with other versions)
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pydantic uvicorn fastapi pyinstaller


5. Run 1b_package.py and/or 3b_package.py to install 1b or 3b model (3b is better but larger); once you complete this step
   you won't need internet for the rest of the steps to run nor in the future
python 1b_package.py
python 3b_package.py

6. Run main.py to start local server (works offline)
python main.py

8. In a separate terminal while main.py is running, cd into the project and send requests/messages via: python wrapper.py "type your message here"
 # Make sure to wrap your message in parentheses
 # Can switch the model you use and the parameters by changing the model name in line 8 of wrapper.py
 # Simply rerun main.py to start a fresh conversation
 

   
