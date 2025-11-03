

## Các bước thực hiện

1. Tạo môi trường database: Tải PostgreSQL client và connect nó với AlloyDB instance
```
sudo apt-get update
sudo apt-get install --yes postgresql-client
```

```
export PGUSER=postgres
export PGPASSWORD=samplepassword
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-east1
export ADBCLUSTER=alloydb-aip-01
export INSTANCE_IP=$(gcloud alloydb instances describe $ADBCLUSTER-pr --cluster=$ADBCLUSTER --region=$REGION --format="value(ipAddress)")
```