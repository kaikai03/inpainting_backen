##rabbitmq##

安装
    
    docker pull rabbitmq:3.8.8-management

加载

	docker run -itd --name rbmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=root -e RABBITMQ_DEFAULT_PASS=root1 rabbitmq:3.8.8-management
    docker run -rm --name rbmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=root -e RABBITMQ_DEFAULT_PASS=root1 rabbitmq:3.8.8-management

进入

	docker exec -i -t rbmq /bin/bash

安装后台

	rabbitmq-plugins enable rabbitmq_management
	
##redis##

    docker pull redis
    docker run -itd -p 5673:6379  --name rds  redis  --requirepass "Adminixxx"