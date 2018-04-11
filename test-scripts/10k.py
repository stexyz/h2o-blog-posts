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
# ----10k HIVE ----
h2o.connect(ip=sys.argv[1], port=sys.argv[2])
select_query_10k = "select * from db10k"
start10k = time.time()
ds10k = h2o.import_sql_select(connection_url, select_query_10k, username, password)
end10k = time.time()
print '================results for 10k rows==============='
print 'Hive: the import of 10k rows took', end10k-start10k,'s'
print '================results for 10k rows==============='
