import pandas as pd
from pathlib import Path



frames={}
for filename in list(Path(".").glob("**/*.csv")) :
    frames[str(filename).replace('results/haarcascade_frontalface_','').replace(".xml.csv","")]=pd.read_csv(str(filename),index_col='filename')

ll=list(frames.keys())

data=frames[ll[0]].join(frames[ll[1]],rsuffix="_"+ll[1], how="outer")
print(data.columns)


for k in ll[2:] :
    data=data.join(frames[k],rsuffix="_"+k,how="outer")
    print(data.columns)

data.rename(columns=dict([(a,a+"_"+ll[0]) for a in frames[ll[0]].columns]),inplace=True)


for k in ll :
    o=set(ll)
    o.discard(k)
    print("in {}: {}".format(k, len(data.query("faces_{}>0".format(k)))))
    print(">1 in {}: {}".format(k, len(data.query("faces_{0}>1".format(k)))))
    print("only in {}: {}".format(k, len(data.query("faces_{}>0 and ({})".format(k," and ".join(("faces_{}==0".format(kk) for kk in o)))))))


dd=data.query(" and ".join(["faces_{}==0".format(k) for k in ll])).index
import sys
sys.stdout.write("\n".join(dd))

