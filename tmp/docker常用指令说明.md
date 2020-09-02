##windows 安装##
在windows下除了win10，需要通过`Docker_ToolBox`来运行`docker`。
`Docker_ToolBox`实际上打包了`Oracle VM VirtualBox`、`git`和`docker`。

如果之前安装过git，Docker_ToolBox的安装过程会将旧的git删除，再安装新的。这时候有可能会出现一个意外，它会讲git安装在原有的git目录内，但docker的“快捷方式”中使用的却是C盘下的git默认安装地址（至少至产品版本：18.03.0-ce）。

如果之前电脑没摆弄过虚拟机之类的事，默认情况下，主板的虚拟化支持是disable的，需要去bios把VT-X打开。

默认情况下，docker虚拟机文件创建在`C:\Users\xxxx\.docker`内。对于C盘空间不足的同学，可以先创建系统环境变量`MACHINE_STORAGE_PATH`，用于指明虚拟机创建位置。当然事后创建环境变量和移动也是可行的，把.docker下的文件拷贝到后指定的位置，进入`Oracle VM VirtualBox`删除旧虚拟机即可。

##linux 安装##

linux 要求 3.10内核以上，

	yum update 
	yum install -y yum-utils device-mapper-persistent-data lvm2 # 安装包和驱动管理工具
	yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo #添加docker官方源
	yum install docker-ce-17.12.1.ce-1.el7.centos
	
	systemctl start docker #启动
	systemctl enable docker #加入开机启动

	docker version 验证（有client和service两部分表示docker安装启动都成功了）

安装前确认没有旧版本的docker，否则会导致安装报错
旧版本卸载

	yum erase docker-ee-xxx:x.xx.x.xxxxxxxxx.el7.centos.x86_64

##使用##
运行一个容器

	docker run $镜像名
	
	docker run --env <key>=<value> $镜像名  

`--env` 相当于实时插入环境变量
一个容器的运行可以想象为一个进程，当然它实际上也是一个进程。和一般程序一样，它执行完成之后就退出了。

所以如果容器内所执行的“内容”如果没有“死循环”，那么用`docker ps`并不会看到它。需要通过`docker ps -a`或者`docker ps -n`来查看。

	docker run -i -t $container /bin/sh

可以直接进入容器，这时候只要不`exit`，容器将会一直运行（和ssh执行程序一个概念）。

	docker run --name $name -d $container /bin/sh -c "while true; do echo hello world; sleep 30;done"

`-d`让容器在后台运行，通过bash执行一个“死循环”，可以让容器一直再运行不会退出。

	docker logs [$容器id|$容器name]
	docker attach [$容器id|$容器name] 

在container外面查看它的输出，前者一次性打印全部并结束任务；后者浏览当前时点往后持续监视。
	
	docker exec -it -d [$容器id|$容器name] /bin/sh

容器进程如果还活着，可以通过以上方法再进入容器。

    `-d` will create a container with the process detached from our terminal
	`-P` will publish all the exposed container ports to random ports on the Docker host
	`-e` is how you pass environment variables to the container
	`--name` allows you to specify a container name
	`AUTHOR` is the environment variable name 

文件拷贝

	docker cp [$容器id|$容器name]:/$容器内地址 ./本机目录
	docker cp ./本机目录 [$容器id|$容器name]:/$容器内地址

挂载容器外空间（既本机空间）。有些时候我们希望容器升级或变化的时候，不改变我们的历史数据，则历史数据需要放置在容器外部。

	docker run -v /本机目录:/容器目录  -v /本机目录/文件.后缀:/容器目录/文件.后缀 $镜像名

	例：docker run -v /data/docker/registry:/var/lib/registry  -v /data/docker/config.yml:/etc/docker/registry/config.yml $镜像名

	注意：当文件及目录初始不存在时，docker会帮着创建，但在挂载文件时会有一个问题，它会把文件创建成目录导致运行出错。所以此时需要事前手动去touch一个文件出来。

显示docker的ip映射，开放端口

	docker port $container_name


将容器的80端口映射到本机的1111端口上，既访问本机的1111相当于访问容器的80.

	docker run --name $name -e AUTHOR="Your Name" -d -p 1111:80 $container_name

	docker run -d -p 5000:5000 $container_name
	docker run -d -p 222:333 $container_name
	docker run -d -p 127.0.0.1:5000:5000/udp $container_name
	docker run -d -p 127.0.0.1::5000 $container_name

容器打包成镜像

	docker commit -a "作者" -m "描述" [$容器id|$容器name]  镜像名:tag 

容器停止及移除

	docker stop $container_name
	docker rm $container_name
	# 停止/删除所有
	docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)

	docker rmi <image id>

其他

	docker search
	docker pull ubuntu:12.04

##Dockerfile##

    FROM         指定基础镜像
    MAINTAINER   指定维护者信息
    RUN          在命令前面加上RUN
    ADD          COPY文件，会自动解压
	COPY     同上，不自动解压，注意如果是目录，不会复制最外层目录
    WORKDIR  设置当前工作目录，类似于cd
    VOLUME   设置卷，挂载主机目录
    EXPOSE   指定对外的端口
    CMD      指定容器启动后要干的事情

dockerfile中可以有多条cmd命令，但只是最后一条有效

	docker run -i -t myimage /bin/ps

后面的“/bin/ps”会覆盖掉CMD命令。


创建镜像

	docker build -t 域/名 ./当前路径

查看容器名

	docker inspect [$容器id|$容器name] 
 

使用虚拟机时，虚拟机默认本机访问地址是192.168.99.100，
如果需要被外网访问，则需要去`oracle VirtualBox`的工具里对虚拟机进行设置，
`设置`->`网络`->`高级`->`端口转发`，触发防火墙规则后允许即可。



##私有仓库
linux开放防火墙端口
	firewall-cmd --add-port=5000/tcp 
	firewall-cmd --reload
	servcie restart docker  或 /sbin/service docker restart

	由于部分系统机制，firewall重启后的规则有可能不影响先启动的程序，所以docker也需要重新启动

建立私有仓库
	
	第一次启动，
	docker run --name docker-registry -d --restart=on-failure registry

	用进入容器，把config.yml拷贝到容器外，
		docker exec -i -t docker-registry /bin/sh 
	或直接用docker cp 把默认配置文件拷贝出来
		docker cp docker-registry:/etc/docker/registry/config.yml /data/docker/config.yml
	
	进行修改（见下），然后挂载到容器上。

	注意：缺少config.yml文件会无法挂载，必须先去启动容器中把默认的配置文件拷贝出来
	
	docker stop docker-registry
	docker rm docker-registry
	
	然后正常启动
	docker run --name docker-registry -d --restart=on-failure -p 5000:5000 -v /data/docker/registry:/var/lib/registry  -v /data/docker/config.yml:/etc/docker/registry/config.yml registry

	
修改仓库配置，支持镜像删除
	
	config.yml 中 storage: delete: enabled: 改为true

增加http推送

	注意：应该是客户机修改。也有可能是客服机与服务器都需要改。
	如果用虚拟机的话，需要进入虚拟后才能进行修改。
	docker-machine ssh default 

	在/etc/docker/目录下创建daemon.json文件。在文件中写入：
	{ "insecure-registries":["服务ip:5000"] }

	
	重新加载配置信息再重启docker服务：
	systemctl daemon-reload;
	systemctl restart docker 或  /sbin/service docker restart  或 sudo /etc/init.d/docker restart

私有推送：

	docker push 192.168.1.111:3333/name

访问私有仓库

	docker pull 192.168.1.28:5000/nlp_server:0.1.1_shet_xinnei
	或直接run
	docker run --name $name -p 8080:8080 -idt 192.168.1.111:3333/name

查看镜像

	curl -X GET http://192.168.1.28:5000/v2/_catalog
	curl -X GET http://192.168.1.28:5000/v2/image_name/tags/list

	curl -X GET http://192.168.1.28:5000/v2/<镜像名>/manifests/<tag> --header "Accept: application/vnd.docker.distribution.manifest.v2+json"
	
删除远程镜像

	DELETE /v2/<name>/manifests/<reference>

	curl -I -X DELETE http://192.168.1.111:3333/v2/name/manifests/sha256:6a67ba482a8dd4f8143ac96b1dcffa5e45af95b8d3e37aeba72401a5afd7ab8e

	或
	curl -X DELETE http://localhost:5000/v2/name/tags/latest

删除镜像并不会释放空间，需要执行垃圾回收

	docker exec 进入容器
	/bin/registry garbage-collect /etc/docker/registry/config.yml 