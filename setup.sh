#!/bin/bash
mkdir UncompressedData

#!/bin/bash
FILE_PATH=Data/*
DESTINATION_PATH=UncompressedData/

for FILE in $FILE_PATH
do
    unzip $FILE -d $DESTINATION_PATH
    echo $FILE
done

cp preprocessData.py UncompressedData/

cd UncompressedData
python preprocessData.py
rm preprocessData.py
cd ..

mv UncompressedData ProcessedData

