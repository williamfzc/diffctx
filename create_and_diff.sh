#!/bin/sh
set -e

cd /github/workspace
ls
git config --global --add safe.directory /github/workspace
git status
lsif-go -v
srctx diff
