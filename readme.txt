testmachine11-11
改变srv端口为:1988(config.ini可配置)
改变文件已包形式发送,包格式<I(4长度整包长度)H(包类型)
	包类型:
	0x0001	指令包
	0x0002	返回包
	0x0003	文件包 H(文件名长度)s(文件名)s(文件内容)
增加了传送前的rar的压缩功能
增加clt的list中可以添加特别端口(:分隔)
增加了返回信息
==================================
testmachine11-15
clt设置timeout值为1秒
slt修改收包方式为轮训检测
clt增加了收包完成提示
srv增加了log收集完成提示
==================================
testmachine11-18
clt如果收包超过30秒则自动放弃继续收包
srv和clt进行优化
==================================
testmachine1-20
可以在上传log的文件名上使用相对路径
===================================
testmachine2-16
原server改为client
原client改为control
新架构增加server角色,所有信息通过server中转
支持自动脚本的虚拟Message功能
增加心跳机制,server产生心跳发送至test_manage端
test_manage端连入后收到心跳包后返回,server延时15秒后再次发送心跳包
0x0003,0x0004将会把文件每600byte分割(settings中可设置)为小包发送至server
新增包:
	0x0004	上传文件包
	0x0005	询问链接包
	0x0006	test_manage心跳包
	0xffff	client尾包
	0xff00	control尾包
新增who特殊事件来询问与server正链接的client列表
list中设置all可以对链接server的client进行操作
独立了package.py用来生成数据包
===================================
testmachine2-18
新增包:
	0xf0f0	关闭server
control可在step中新增shutdown来正常退出server.py
who询问中的第二部分表示的是该keyword下的channel数
===================================
testmachine2-21
client端中config.ini文件中需要输入相应账号密码
可以协助gm-uas脚本做到游戏进程自动开关
===================================
testmachine2-27
settings中VirtualMessage是关闭和打开虚拟message服务器的开关
===================================
testmachine3-14
控制端的config.ini中添加步骤conf用来对客户端段的config.ini的单项行进修改
===================================
testmachine3-23
修复了端口为172的错误
详细了error日志
控制端增加了响应统计信息
gmclient_watcher可以检测到gmclient的信息发现相应错误并截屏
修复在执行中heart time out问题
修改心跳超时时间为60秒
===================================
testmachine3-28
在config.ini的service域添加了status项，用来切换程序在debug模式和release模式之间
===================================
testmachine3-29
控制端的config.ini文件中list列表的首字符为"!"，则该列表为取反列表
===================================
testmachine3-31
添加了与GMClient心跳检测
===================================
testmachine5-5
修复因为大文件压缩而导致的心跳检测超时