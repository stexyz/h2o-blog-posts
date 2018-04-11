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
# ----100M HIVE ----
#h2o.init(extra_classpath=["/usr/lib/hive/jdbc/hive-jdbc-2.3.2-amzn-1-standalone.jar"])
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
select_query_100M = "select * from db100M"
start100M = time.time()
ds100M = h2o.import_sql_select(connection_url, select_query_100M, username, password)
end100M = time.time()
print '================results for 100M rows==============='
print 'Hive: the import of 100M rows took', end100M-start100M,'s'
print '================results for 100M rows==============='
