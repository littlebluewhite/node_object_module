git config --global credential.helper cache 'cache --timeout=30'
git pull
git credential-cache exit
docker-compose up -d --build
