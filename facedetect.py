#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import cv2
import click
import logging
import sys
import csv


logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)
logger=logging.getLogger(__name__)


# local modules
# from video import create_capture
from common import clock, draw_str


def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=4, minSize=(20, 20),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

fields=['faces','eyes','seconds','filename']

@click.command()
@click.argument('files',nargs=-1)
@click.option('-c','--cascade',default='cascades/haarcascade_frontalface_alt.xml')
@click.option('-n','--nested',default='cascades/haarcascade_eye.xml')
@click.option('-d','--detected/--no-detected',default=False,help="show only detected faces")
@click.option('--show/--no-show',default=True,help="do not show images, only count")
@click.option('--stats',default=None,type=click.File('w'),help="pipe stats to FILE (use - for STDOUT)")
@click.option('-l','--loglevel',type=click.Choice(['DEBUG','INFO','WARN']),default='INFO')
def facefinder(files,nested=None,cascade=None,detected=False,show=True,loglevel='INFO',stats=False) :
    cascade = cv2.CascadeClassifier(cascade)
    nested = cv2.CascadeClassifier(nested)
    logger.setLevel(getattr(logging,loglevel))
    if stats :
        logger.debug("Stats is {}".format(type(stats)))
        wr=csv.writer(stats.open())
        wr.writerow(fields)
    else :
        wr=False
    for f in files :
        try :
            img = cv2.imread(f)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            t = clock()
            logger.debug("Starting detection on {f}".format(**locals()))
            rects = detect(gray, cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))
            subrects=[]
            if not nested.empty():
                for x1, y1, x2, y2 in rects:
                    roi = gray[y1:y2, x1:x2]
                    vis_roi = vis[y1:y2, x1:x2]
                    subrects = detect(roi.copy(), nested)
                    draw_rects(vis_roi, subrects, (255, 0, 0))
            thisstats=[len(rects),len(subrects),clock()-t,f]
            logger.info("Detected: {} faces, {} eyes in  {} ms on {}".format(*thisstats))
            if wr :
                wr.writerow(thisstats)
            if show and (len(rects)>0 or not detected) :
                dt = clock() - t

                draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
                cv2.imshow('facedetect', vis)
                e=cv2.waitKey(0)
                cv2.destroyWindow('facedetect')
                if e == 27 :
                    break
        except Exception as e:
            logger.exception("{} while processing {}".format(e,f))
    stats.close()


if __name__ == '__main__':
    facefinder()

