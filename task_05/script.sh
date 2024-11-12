echo "Create git user-group"
sudo groupadd -g 1500 git
sudo useradd -m -u 1500 -g 1500 git

echo "Install docker"
curl -fsSL https://get.docker.com/ | sh
systemctl start docker
sudo usermod -aG docker git

echo "Install git lfs"
sudo apt update -y && sudo apt install -y git git-lfs && git lfs install

mkdir gitea
chown git:git gitea

echo "Run gitea & Minio"
docker network create gitea
docker run -d \
    --name gitea \
    --network gitea \
    --restart always \
    -e USER_UID=1500 \
    -e USER_GID=1500 \
    -v /home/git/.ssh:/data/git/.ssh \
    -v /etc/timezone:/etc/timezone:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -p 3000:3000 \
    -p 2222:22 \
    gitea/gitea

docker run -d \
    --name minio \
    --network gitea \
    -v $(pwd)/storage:/data \
    -p 9000:9000 \
    -p 9001:9001 \
    maverick0809/minio \
    server --console-address ":9001" /data

 
