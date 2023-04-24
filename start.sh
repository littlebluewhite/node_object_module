git config --global credential.helper cache 'cache --timeout=30'
git pull
git credential-cache exit
sudo chmod -R 777 deploy/
docker-compose down
docker-compose up -d --build
