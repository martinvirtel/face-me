SHELL := /bin/bash
.PHONY :  test 


TRY := cascades/haarcascade_frontalface_alt2.xml cascades/haarcascade_frontalface_alt_tree.xml cascades/haarcascade_frontalface_alt.xml cascades/haarcascade_frontalface_default.xml


test : 
	for cascade in $(TRY) ; do  \
	  python ./facedetect.py --no-show --loglevel=WARN --cascade=$$cascade --stats=results/$$(basename $$cascade).csv images/WhoIsUnlocking/*jpg ; \
	done

none.txt : analyze.py
	python ./analyze.py | sed -n '/image/p' > none.txt


links : none.txt
	rm ./images/none/* ;\
	cat none.txt | xargs -l1 -I\@ ln \@ ./images/none/ 

annotate : 
	/usr/local/bin/opencv_annotation --annotations=/home/martin/projekte/who_is_unlocking/images/$$(date +%Y%m%d%H%M%S).txt --images=/home/martin/projekte/who_is_unlocking/images/none/
