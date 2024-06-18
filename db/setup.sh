sudo docker build -t swgoh_image ./db
sudo docker run --name swgoh_container -e POSTGRES_PASSWORD=password -d swgoh_image



