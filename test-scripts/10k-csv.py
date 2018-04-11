# ----common init----
import h2o
import sys
import time
import socket
ip=socket.gethostbyname(socket.gethostname())
# ----10k CSV ----
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
start10kcsv = time.time()
ds10kcsv = h2o.import_file("hdfs://"+ip+"/user/hadoop/10k/data10k.csv")
end10kcsv = time.time()
print '================results for 10k rows==============='
print 'HDFS: the import of 10k rows from CSV/HDFS took', end10kcsv-start10kcsv,'s'
print '================results for 10k rows==============='
