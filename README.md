# Analysis GIT Repository

This Program analysis commits in a git repo and finds the top 12 modified modules in a directory over the past 6 months

## Installation

The program uses GitPython & Progress Bar package. You can install them using the commands below. 

```bash
pip install gitpython
pip install progress
```

## Usage

In order to use the program, you will need to provide it with two arguments. The first argument is the relative location of the git repository containing .git  and the second argument is the name of the directory you want to analyze. For example, for the following working directory we want to analyze working_dir/nova/nova

working_dir
    |_ repo_analysis
       |_ main.py
       |_ README.md
	|_ nova
	   |_ .git
	   |_ api-guide
	   |_ doc
	   |_ etc
	   |_ nova

We will use the following command line to call our program

```bash
python main.py ../nova nova
```

Getting churns per commit takes time. Hence, if the progress bar doesn't show up in your terminal for any reason, please wait it is not stuck.

## Output
The program will print out two lists of modules. The first list will show all modules with highest number of commits and the second list outputs the modules with highest churns

## License
[MIT](https://choosealicense.com/licenses/mit/)