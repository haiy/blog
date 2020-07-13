---
title: hack ssh
date: 2016-10-02 00:00:00 Z
layout: post
---

{{page.title}}
=============

<p class="meta">2 Oct 2016</p>

<pre>
机器	IP	备注
A	10.21.32.106	目标服务器，处于内网
B	22.12.23.123	外网服务器，相当于桥梁的作用
C 外网主机
</pre>
目标：从 C 机器使用 SSH 访问 A


# 反向ssh隧道操作
——————————————————

```
#A 上执行
ssh -fNTR 2210:localhost:22 root@ecs
B执行
ssh -p 2210 pi@localhost
```


#ssh 反向代理

```
#A 上执行
ssh -fCNR [B机器IP或省略]:[B机器端口]:[A机器的IP]:[A机器端口] [登陆B机器的用户名@服务器IP]
ssh -fNTR 1234:localhost:4000 root@ecs

#B执行
ssh -fCNL [B机器IP或省略]:[B机器端口]:[B机器的IP]:[B机器端口] [登陆B机器的用户名@B机器的IP]
ssh -fCNL *:4000:localhost:1234 localhost
```

# ssh reverse proxy smb/samba

smb 是139端口

# keep long ssh connection live

```
Host *
   ServerAliveInterval 108000
```   

# 添加系统启动

```
vi /etc/rc.d/rc.local
autossh -M 2211 -fCNR 2222:localhost:22 root@ecs
chmod +x /etc/rd.d/rc.local
```

 其中samba在端口转发的生时候因为是系统端口，小于1000，所以要使用sudo来进行转发，sudo的时候用到的ssh信息是root的，
 所以这时候很容易出现的一个问题是因为root的id_rsa.pub的ssh key没有添加无法成功。如果不能成功的建议在ssh的时候加上debug
 信息，并去掉 -f 选项。


### Refs
- <https://www.ssh.com/ssh/command/>  
- <https://toic.org/blog/2009/reverse-ssh-port-forwarding/>   
- <http://askubuntu.com/questions/598626/direct-ssh-tunnel-through-a-reverse-ssh-tunnel>  
- <https://unix.stackexchange.com/questions/46235/how-does-reverse-ssh-tunneling-work>  
- <https://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html>  
- <https://blog.csdn.net/mitant/article/details/10714699>  
- <https://www.cnblogs.com/kwongtai/p/6903420.html>  
- <http://ibiblio.org/gferg/ldp/Samba-with-SSH/Samba-with-SSH-4.html>  
