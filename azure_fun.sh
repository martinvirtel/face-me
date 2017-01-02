#! /bin/bash

echo Detected/Undetected:
ls -l azure_face_detection/*json | counter.py 'martin [ 1]' | sed '1d;s/martin 1/detected/;s/martin  /undetected/'


echo Age distribution:
cat azure_face_detection/*json | jq '.[]|.faceAttributes.age'  | counter.py '(?P<age_float>.*)'
