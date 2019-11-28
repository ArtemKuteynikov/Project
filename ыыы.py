import subprocess as sbp
import pip
sbp.run('python -m pip install --upgrade pip')
sbp.run("pip install -r reqs.txt" )