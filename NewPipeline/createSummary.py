

import subprocess

# Define command and arguments
command = 'Rscript'
path2script = '/Users/granthussey/github/MitoScripts/MitoScripts/NewPipeline/extractData.R'

# Variable number of args in a list
mitograph_output_directory = '/Users/granthussey/github/MitoScripts/MitoScripts/data/'

# Build subprocess command
subprocess_command = [command, path2script] + mitograph_output_directory

# check_output will run the command and store to result
subprocess.(cmd, universal_newlines=True)
