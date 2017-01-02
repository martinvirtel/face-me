import requests
import logging
import datetime
import os
import click
import json

HERE=os.path.split(__file__)[0]

import logging,sys
logger=logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr,level=logging.DEBUG,format='%(asctime)-15s %(filename)s:%(lineno)s %(message)s')


from credentials import facedetect_subscription_key

def detect_face(filename) :
    url='https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=true&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses'
    headers={ 'Content-type' : 'application/octet-stream', 'Ocp-Apim-Subscription-Key' : facedetect_subscription_key }
    with open(filename,"rb") as f :
        response=requests.post(url,f,headers=headers)
    return response.json()



@click.command()
@click.argument('filename')
def print_detected_face(filename) :
    """
    input parameter: filename for image file
    output: JSON on STDOUT
    """
    r=detect_face(filename)
    sys.stdout.write(json.dumps(r))



if __name__ == '__main__' :
    print_detected_face()






