##Harbor 安装指南

条件，安装Docker后

默认docker-ce不含docker-compose 组件 

需要
	
	pip install docker-compose

如果 pip 未安装， 可先 
	
	yum -y install pip

harbor下载地址

	https://github.com/goharbor/harbor/releases

解压后修改配置文件
	
	/harbor/harbor.cfg
	
	有必要改的配置项：
	hostname 本服务地址，不能写127.0.0.1否则外部客户端无法登录。
	harbor_admin_password admin初始密码。注意初始密码只能使用一次，登录后即时更改，否则下次admin帐号无法登录。
	

修改完成后

	./prepare
	./install.sh

安装完成既启动，在harbor文件夹中执行`docker-compose ps` 可查看运行状态。


奇怪的是harbor包含很多其他工具组件docker镜像，但是这些东西的启动参数并不是永久驻留的，也就是说重启docker或者系统时，它很多组件并不会自启动。



##docker 对应修改

docker增加http推送，因为docker默认传输是HTTPS，需要用http要增加非安全信任。

	注意：客服机与服务器都需要改。
	如果用虚拟机的话，需要进入虚拟后才能进行修改。
	docker-machine ssh default 

	在/etc/docker/目录下创建daemon.json文件。在文件中写入：
	{ "insecure-registries":["服务ip"] }

	
	重新加载配置信息再重启docker服务：
	systemctl daemon-reload;
	systemctl restart docker 或  /sbin/service docker restart  或 sudo /etc/init.d/docker restart



## 上传镜像

上传镜像：登录harbor，在项目下，展开`推送镜像`，可看到命令的例子。

	docker push 192.168.1.28/项目名/IMAGE[:TAG]

上传镜像时，需要进行登录

	docker login 192.168.1.28
	帐号密码使用harbor上创建的帐号密码

	login参数 注意一定要填写源地址，否则默认情况下登录的目标为docker官方的hub

## 下载镜像
	
Harbor上新建项目时，如果选中公开选项，则下载镜像时无需登录。

	docker pull 192.168.1.28/项目名/IMAGE[:TAG]


## 其他

重启hardor

	docker-compose stop
	docker-compose start

	或 docker-compose restart

删除hardor

	除了删除hardor文件和docker rm相关镜像外，
	还有hardor的数据库和上传的镜像
	数据库位置：/data/database
	镜像文件位置：/data/registry

28的管理员账户
	admin  Admin123456