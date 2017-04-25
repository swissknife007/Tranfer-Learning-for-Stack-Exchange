#!/bin/bash
rm -rf UncompressedData
rm -rf ProcessedData
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
touch physics
for FILE in ./*
do
    echo $FILE
    sed -i 's/ \+/ /g' $FILE
    sed -i '1d' $FILE
    TAGFILE=`echo $FILE | cut -d'_' -f1`
    cut -d',' -f4 $FILE > temp
    sed -i 's/"//g' temp
    sed -i 's/ /\n/g' temp
    sort temp|uniq > $TAGFILE
    rm temp
done
cd ..

mv UncompressedData ProcessedData

