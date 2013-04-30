import json
import pickle
import hashlib
from jsonconfig import JsonConfig


CONFIG_FILE = 'a.txt'
jc = JsonConfig(CONFIG_FILE)
print jc.read()
jc.config = {'consumer_key': 'ttttttttt', 'access_token': 'yyyyyyyy'}
jc.save()
print jc.read()

s="it is a str"
print hashlib.sha256(s).hexdigest()

a={'1':"11",'2':"22"}
for tt in a:
    print tt,"===",a[tt]
ff=open('hashid.txt','w')
pickle.dump(a,ff)
ff.close()
gg=open('hashid.txt','r')
ag=pickle.load(gg)
print ag
print ag['1'], ag['2']
gg.close()


a={'1',"11",'2',"22"}
ff=open('hashidtt.txt','w')
pickle.dump(a,ff)
ff.close()
gg=open('hashidtt.txt','r')
ag=pickle.load(gg)
print ag
list2=list(ag)
print list2
gg.close()

a1="ttt"
b1="ttt"
if a1==b1:
    print "equal"
else:
    print "not equal"