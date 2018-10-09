generate doc
------------

in /pydgrid/docs/ run:
sphinx-build ./source ./generate



https://mybinder.org/v2/gh/pydgrid/pydgrid/master


python setup.py sdist upload

pip install pydgrid --upgrade


bug fix
-------

see: pydgrid/docs/dev/nvie-git-workflow-commands.png

make changes

change version in /pydrgid/__init__.py

git add . 
git commit -m '
python setup.py sdist upload

