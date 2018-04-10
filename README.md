# Performance Testing Hive Data Ingestion on Amazon EMR

Since the 3.20.0.1 release H2O supports Hive as a possible data source through the JDBC driver. As a part of that a performance test was conducted comparing ingestion of data from CSV file on HDFS and Hive DB.

This post describes how to set up the environment and run the comparison. 

## Setting up cluster
A guide can be found [here](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html).
We have used 6 m4.large machines with 2 cores and 8GB RAM each. 

### Security Groups
Go to the [EC2 Dashboard](https://eu-central-1.console.aws.amazon.com/ec2/v2/home?region=eu-central-1#Home:). In order to SSH onto the cloud master the security group setting needs to be changed. Go to `NETWORK & SECURITY > Security Groups -> "ElasticMapReduce-master"` and in the "Inbound" tab click Edit. Add new Rule for SSH with IP/32 (=valid CIDR for the only 1 IP address).

On your local machine remove access on the private key (.pem file) to only have read yourself (`chmod og-x mykey.pem`)

**Note:** Remember to reset the cluster to avoid extra charges like  [here]([https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs-reset-environment.html).

## Data
It makes sense to use some data that corresponds to your use case. We have used a data set of first 10k rows of airlines data from [here](https://s3.amazonaws.com/h2o-public-test-data/smalldata/airlines/AirlinesTest.csv.zip) and then created semi synthetic data by repeating the pattern as needed (see script below). 

### Create data
Upload the `10k.csv` (10k rows without header), `header.csv` (just one header row) to the EMR master. To store files locally run the script from `/mnt/s3` as there is enough space:

```
#!/bin/bash
rm data*
echo 10k
head -n 1 header.csv >> data10k.csv
tail -n 10000 10k.csv >> data10k.csv

echo 100k
head -n 1 header.csv >> data100k.csv
for (( c=1; c<=10; c++ ))
do  
	echo iteration $c / 10
	tail -n 10000 10k.csv >> data100k.csv
done
wc data100k.csv

echo 1M
head -n 1 header.csv >> data1M.csv
for (( c=1; c<=10; c++ ))
do  
	echo iteration $c / 10
	tail -n 100000 data100k.csv >> data1M.csv
done
wc data1M.csv

echo 10M
head -n 1 header.csv >> data10M.csv
for (( c=1; c<=10; c++ ))
do  
	echo iteration $c / 10
	tail -n 1000000 data1M.csv >> data10M.csv
done
wc data10M.csv

echo 100M
head -n 1 header.csv >> data100M.csv
for (( c=1; c<=10; c++ ))
do  
	echo iteration $c / 10
	tail -n 10000000 data10M.csv >> data100M.csv
done
wc data100M.csv
```

### Upload the files to HDFS to separate directories
```
#!/bin/bash
hdfs dfs -mkdir /user/hadoop/10k
hdfs dfs -put /user/hadoop/10k/data10k.csv
hdfs dfs -mkdir /user/hadoop/1M
hdfs dfs -put /user/hadoop/1M/data1M.csv
hdfs dfs -mkdir /user/hadoop/100M
hdfs dfs -put /user/hadoop/100M/data100M.csv
```
### Create anonymous home on HDFS (to run queries)
To be able to run Hive queries we need to create home folder for the anonymous user on HDFS.
```
#!/bin/bash
hdfs dfs -mkdir /user/anonymous
hdfs dfs -chown anonymous:anonymous /user/anonymous
```
### Create Hive DBs for the 10k, 1M, 10M and 100M data sets
1. use client to connect to default db on localhost: `beeline -u jdbc:hive2://localhost:10000/default`
(alt. just run `beeline` and call `!connect jdbc:hive2://localhost:10000/default`)
1. create 4 DBs (10k, 1M, 10M, 100M)

**Note:** the `LOCATION '/user/hadoop/10k'` clause makes sure that the file on HDFS is used as underlying storage for the DB in Hive (and is kept in place so we can later access it through HDFS as well).
Run the following script for all the tables (not just DB10k)
```
CREATE EXTERNAL TABLE IF NOT EXISTS DB10k(
fYear STRING ,
fMonth STRING ,
fDayofMonth STRING ,
fDayOfWeek STRING ,
DepTime INT ,
ArrTime INT ,
UniqueCarrier STRING ,
Origin STRING ,
Dest STRING ,
Distance INT ,
IsDepDelayed STRING ,
IsDepDelayed_REC INT)
COMMENT 'hive-test-table 10k'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '/user/hadoop/10k';
```

## Setup H2O
A detailed description can be found [here](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/downloading.html#install-in-python)
**note**: for some reason there is no symlink for super user for pip on EMR master ([details](https://unix.stackexchange.com/questions/169251/root-shell-sees-pip-but-sudo-pip-command-not-found))
```
sudo ln -s /usr/local/bin/pip /usr/bin/pip
sudo ln -s /usr/local/bin/pip2 /usr/bin/pip2
sudo ln -s /usr/local/bin/pip2.7 /usr/bin/pip2.7
pip install requests
pip install tabulate
pip install scikit-learn
pip install colorama
pip install future
pip install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o
```

## Import data to H2O
The JDBC driver is at `/usr/lib/hive/jdbc/hive-jdbc-2.3.2-amzn-1-standalone.jar`.

### H2O Cluster
To run H2O in cluster we need the `h2odriver.jar`. As for Apr 2018, EMR works well with [HDP 2.6](http://h2o-release.s3.amazonaws.com/h2o/rel-wolpert/5/h2o-3.18.0.5-hdp2.6.zip
) version of H2O driver.
`wget http://h2o-release.s3.amazonaws.com/h2o/rel-wolpert/5/h2o-3.18.0.5-hdp2.6.zip`

Max memory for the 8GB machines that was available for H2O was 5G.
`hadoop jar h2o-3.18.0.5-hdp2.6/h2odriver.jar -libjars /usr/lib/hive/jdbc/hive-jdbc-2.3.2-amzn-1-standalone.jar -nodes 3 -mapperXmx 5g`

**note:** Get the IP address and port of the cloud leader (line like this):
`H2O node 172.31.31.246:54321 reports H2O cluster size 3 [leader is 172.31.18.72:54321]`
Use that as a parameter in the Python test script.
After each run of following scripts stop the cluster and start it over again.

### Hive test
Call it with parameters (ip, port). The IP taken from the last section.
Need to run this test with different `select_query_10k` values to excercise all sizes of data.
```
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
```
### CSV test
Again, call it with parameters (ip, port). Need to run this test with different versions of CSV file (`h2o.import_file("hdfs://"+ip+"/user/hadoop/10k/data10k.csv")`).
```
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
```

## Results:

Let me recap the measurement again:
**System:** EMR cluster of 6 M4 large machines (2CPUs, 8GB mem).
**H2O Cluster:** 3 nodes with 5GB mem each.

Comparing CSV import from HDFS vs import of the same data from Hive DB.

Data [rows] | CSV import [s] | Hive import [s]
------------|----------------|----------------
10000 | 2.6 | 20.6
1000000 | 6.8 | 35.3
10000000 | 14.8 | 121.0
100000000 | 100 | DNF (memory pressure*)

(* the import of 100M rows took aprox 20 minutes to finish to 100% state in console, but slowed down due to mem.pressure (swapping and GC records in log)); should use more memory on the H2O cluster for such large data sets.

**Based on the test the Hive data ingest seems to scale well and can be used on large data sets.**

There are, however, two things to consider:
* constant inherent delay due to the distributed way of computing (penalises small datasets substantially, cannot use efficiently to rapidly build models)
* a lot higher memory requirements (for aprox. 6GB of data the H2O cluster of 3x5GB gets under memory pressure, single node H2O even failed with OOO on 8GB machine)
