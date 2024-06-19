### Working with virtual environments
To install virtualenv package on your system

```bash
pip install virtualenv
``` 

To create a virtual environment named venv inside your project directory

```bash
virtualenv venv
``` 

To activate the virtual environment

```bash
#venv\scripts\activate
#eerst deze
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

#daarna deze
.\venv\Scripts\Activate.ps1
```

To install all the dependencies

```bash
pip install -r requirements.txt
```

To deactivate the virtual environment

```bash
venv\scripts\deactivate
```

To update the requirements.txt file

```bash
pip freeze > requirements.txt
```