./db/setup.sh

sudo docker inspect  -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' swgoh_container > discord_bot/db_ip_addr

./discord_bot/start_api.sh