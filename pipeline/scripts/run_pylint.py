# for python code fromatting best practices
'''Pylint Checks'''
import os
import sys
import logging
from pathlib import Path
from pylint.lint import Run
logging.getLogger().setLevel(logging.INFO)
print(Path(__file__).parent.parent.parent)
ROOT_DIR=Path(__file__).parent.parent.parent
print(ROOT_DIR)
def get_file(top_directory, config=True):
    """Getting File"""
    if config:
        for path, dirs, files in os.walk(top_directory):   #pylint: disable=unused-variable
            for name in files:
                if name == ".pylintrc":
                    return os.path.join(path, name)
    file_paths = []
    for path, dirs, files in os.walk(top_directory):
        for name in files:
            if name.endswith(".py"):
                file_paths.append(os.path.join(path, name))
    return file_paths
CONFIG_FILE = get_file(ROOT_DIR)
FILE_NAMES = get_file(ROOT_DIR, config=False)
FAIL_COUNTER = 0
for file in FILE_NAMES:
    try:
        logging.info(' PyLint | '
                     ' Linting: %s |', file)
        results = Run([file, f"--rcfile={CONFIG_FILE}"], do_exit=False)
        final_score = results.linter.stats['global_note']
        if final_score < 10:
            message = (' Pylint Failed | Failed on : %s | Score: %s ' % (file, final_score))
            logging.error(message)
            FAIL_COUNTER += 1
        else:
            message = (' Pylint Passed | Path %s | Score: %s | ' % (file, final_score))
            logging.info(message)
    except KeyError:
        continue

if FAIL_COUNTER > 10:
    logging.error('%s Files failed pylint checks. Please address and resubmit.', FAIL_COUNTER)
    sys.exit(1)
    