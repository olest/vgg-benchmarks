import argparse
import os.path
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--backend")
args = parser.parse_args()

with open(os.path.expanduser("~/.keras/keras.json"), "w") as fh:
    if args.backend == "theano":
        fh.write('{ "image_dim_ordering": "th", "epsilon": 1e-07, "floatx": "float32", "backend": "theano" }')
    elif args.backend == "tensorflow":
        fh.write('{ "image_dim_ordering": "tf", "epsilon": 1e-07, "floatx": "float32", "backend": "tensorflow" }')
    else:
        print "Backend must be theano or tensorflow"
	sys.exit()

import numpy as np
import time
from keras.optimizers import SGD
from keras.applications.vgg16 import VGG16

width = 224
height = 224
batch_size = 16

model = VGG16(include_top=True, weights=None)
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd) # loss='hinge'

if args.backend == "theano":
    x = np.zeros((batch_size, 3, width, height), dtype=np.float32)
elif args.backend == "tensorflow":
    x = np.zeros((batch_size, width, height, 3), dtype=np.float32)
else:
    print "Backend must be theano or tensorflow"
    sys.exit()

y = np.zeros((batch_size, 1000), dtype=np.float32)

# warmup
model.train_on_batch(x, y)

t0 = time.time()
n = 0
import time
outfile="keras_benchmark_" + time.strftime('%d_%m_%H_%M_%S') + ".csv"
import socket
host = socket.gethostname()
with open(outfile,'w') as out:
    print >>out,"#",host
    while n < 100:
        tstart = time.time()
        model.train_on_batch(x, y)
        tend = time.time()
        print "Iteration: %d train on batch time: %7.3f ms." %( n, (tend - tstart)*1000 )
        print >>out,"%d, %7.3f" %( n, (tend - tstart)*1000 )
        n += 1
t1 = time.time()

print "Batch size: %d" %(batch_size)
print "Iterations: %d" %(n)
print "Time per iteration: %7.3f ms" %((t1 - t0) *1000 / n)
