Author: Hao DUAN<548771> Yu SUN<629341>  
Date: 30 Oct 2015  

Correlation Analysis Program
./Cluster
before run this programs, you have to build following directories 
./clusterimage/day ./clusterimage/daydimention 
./clusterimage/hourcon  ./clusterimage/hourcondimention 

daylevel_cluster_mds.py : draw mds cluster indexed with day data.
daylevel_cluster_pairvariable.py : draw pair varaible cluster indexed with day data.
hourlevel_cluster_mds.py :draw mds cluster indexed with hour data.
hourlevel_cluster_pairvariable.py : draw pair varaible cluster indexed with hour data.
gatherweathertodb.py : a piece code to get weather information from forecast io and save to db


./Timeseries
before run this programs, you have to build following directories 
./correlation/city ./correlation/day  ./correlation/hour 

daylevel_timeseries_analysis.py: find correlation and covariance indexed with day data.
hourlevel_timeseries_analysis.py: find correlation and covariance indexed with hour data.
gatherweathertodb.py: a tool to get weather information from forecast io and save to db