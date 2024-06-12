#!/bin/zsh
rm -R dist/
python -m build
twine upload dist/*
