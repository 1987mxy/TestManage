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
testmachine2-15
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