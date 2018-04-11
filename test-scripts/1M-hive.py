# ----common init----
import sys
import h2o
import time
import socket
#this is localhost IP, through which Hive can be accessed (not the h2o cloud leader)
ip=socket.gethostbyname(socket.gethostname())
connection_url = "jdbc:hive2://"+ip+":10000/default"
username = "hive"
password = ""
# ----1M HIVE ----
#h2o.init(extra_classpath=["/usr/lib/hive/jdbc/hive-jdbc-2.3.2-amzn-1-standalone.jar"])
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
select_query_1M = "select * from db1M"
start1M = time.time()
ds1M = h2o.import_sql_select(connection_url, select_query_1M, username, password)
end1M = time.time()
print '================results for 1M rows==============='
print 'Hive: the import of 1M rows took', end1M-start1M,'s'
print '================results for 1M rows==============='
