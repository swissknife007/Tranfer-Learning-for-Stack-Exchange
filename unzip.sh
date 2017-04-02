#!/bin/bash
FILE_PATH=Data/*

for FILE in $FILE_PATH
do
    unzip $FILE
    echo $FILE
done
