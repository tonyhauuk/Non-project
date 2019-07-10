import pip
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call
import time

for dist in get_installed_distributions():
    print(dist.project_name)
print('-' * 10)

for dist in get_installed_distributions():
    print("updating:", dist.project_name, "\t")
    print(time.asctime(time.localtime(time.time())))
    call("pip3 install --upgrade " + dist.project_name, shell=True)

    '''
    call is not found in the python file
    this is a simple demo file that function is upgrade pip python package
    via python program beyond the code
    '''

