## Setup Instructions  

- Install Python (the lastest stable version is fine). Make sure to **click** the "Add python.exe to PATH" checkbox.

- The following commards should be entered into the terminal: 

    1. create a virtual environment for your project: `python -m venv <your_venv_name>`

    2. Navigate into the \Scripts directory: `cd <your_venv_name>/Scripts` and activate the virtual env: `./activate`. Navigate back `cd ../`

    3. Clone the repo into your venv: `git clone https://github.com/rootdrew27/CS355-GP.git`

    4. Install the dependencies `python -m pip install -r requirements.txt`

- When working on and running the website. Make sure to activate the virtual environment that you created (See step 2). 

- You're Good to Go.

## Run the Website

Using the terminal, while in the project folder, enter: `python app.py`. Then, type *localhost:8000* into your browser

## App Design

- Currently, I am still learning about effective ways to model our app. For now, we will have all html files in the templates folder. (as intended by flask)

- Otherwise, feel free to do whatever.