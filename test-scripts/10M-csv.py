# ----common init----
import h2o
import sys
import time
import socket
ip=socket.gethostbyname(socket.gethostname())
# ----10M CSV ----
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
start10Mcsv = time.time()
ds10Mcsv = h2o.import_file("hdfs://"+ip+"/user/hadoop/10M/data10M.csv")
end10Mcsv = time.time()
print '================results for 10M rows==============='
print 'HDFS: the import of 10M rows from CSV/HDFS took', end10Mcsv-start10Mcsv,'s'
print '================results for 10M rows==============='

