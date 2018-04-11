# ----common init----
import h2o
import sys
import time
import socket
ip=socket.gethostbyname(socket.gethostname())
# ----100M CSV ----
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
start100Mcsv = time.time()
ds100Mcsv = h2o.import_file("hdfs://"+ip+"/user/hadoop/100M/data100M.csv")
end100Mcsv = time.time()
print '================results for 100M rows==============='
print 'HDFS: the import of 100M rows from CSV/HDFS took', end100Mcsv-start100Mcsv,'s'
print '================results for 100M rows==============='
