sudo docker compose down
sudo docker volume rm $(sudo docker volume ls | grep datagrip | awk '{print $2}')
sudo docker volume ls
