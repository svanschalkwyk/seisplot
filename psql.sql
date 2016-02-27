postgres=# -d seismic -c "CREATE EXTENSION postgis;"
postgres-# -d seismic -c "CREATE EXTENSION postgis_topology;"
postgres-# -d seismic -c "CREATE EXTENSION postgis_sfcgal;"
postgres-# -d seismic -c "CREATE EXTENSION fuzzystrmatch"
postgres-# -d seismic -c "CREATE EXTENSION fuzzystrmatch"
postgres-# -d seismic -c "CREATE EXTENSION address_standardizer;"
postgres-# 

delete from nav_meta;
select COUNT(*) from nav_meta