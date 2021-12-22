set -e

# a source code security analysis tool that scans for known vulnerabilities in code written in python

pip3 install bandit
bandit -r .