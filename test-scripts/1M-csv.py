# ----common init----
import h2o
import sys
import time
import socket
ip=socket.gethostbyname(socket.gethostname())
# ----1M CSV ----
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
start1Mcsv = time.time()
ds1Mcsv = h2o.import_file("hdfs://"+ip+"/user/hadoop/1M/data1M.csv")
end1Mcsv = time.time()
print '================results for 1M rows==============='
print 'HDFS: the import of 1M rows from CSV/HDFS took', end1Mcsv-start1Mcsv,'s'
print '================results for 1M rows==============='
