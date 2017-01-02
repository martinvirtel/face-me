#! /bin/bash


for a in $(find images/WhoIsUnlocking/*.jpg ); do
    TARGET=azure_face_detection/$(basename $a).json
    if [ ! -e $TARGET ] ; then
        python ./azure_face_detection.py $a >azure_face_detection/$(basename $a).json
        sleep 5
    else 
        echo $TARGET exists, skipping
    fi
done

