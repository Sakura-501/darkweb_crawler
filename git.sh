#!/bin/zsh
git rm -r --cached .
git add *
git commit -m "$0"
git push