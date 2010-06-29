#!/bin/sh

git tag -l release/* | \
    tail -n1 | \
    cut -d"/" -f2
