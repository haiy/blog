---
title: k8s集群搭建
layout: post
---

{{page.title}}
=============

<p class="meta">18 April 2018</p>

### 环境


master的cpu核数至少2个以上！基本配置有要求.ubuntu，GitVersion:"v1.10.0",


### 操作步骤

- 1 添加锅内的[aliyun的k8s镜像源](https://opsx.alibaba.com/mirror)，适当修改下自己系统的apt源。

    ```bash
    apt-get update && apt-get install -y apt-transport-https
    curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - 
    cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
    deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
    EOF  
    apt-get update
    apt-get install -y kubelet kubeadm kubectl
    ```

- 2 关掉防火墙和swap

    ```bash
    rm -rf /etc/localtime 
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
    systemctl disable firewalld ; service firewalld stop
    cat /proc/swaps
    swapoff
    #修改/etc/fstab永久关掉
    ```

- 3 安装一些基本组件,建议直接在root下操作

    ```bash
    sudo apt-get update \
      && sudo apt-get install -y docker.io  kubelet \
      kubeadm \
      kubernetes-cni
    ```

- 4 代理配置 这个看似容易，实则容易被坑

    鉴于锅内的情况，在启动过程其实需要一些google大佬的镜像的，而这些玩意它不会明确提示你它搞不定，最直接的表现就是假装在努力pull。[Kubeadm init blocks at "This might take a minute or longer if the control plane images have to be pulled](https://github.com/kubernetes/kubeadm/issues/684).

    解决方法就是添加代理。需要添加的代理有两个部分: 一个是docker，另一个是kubeadm。代理最好直接用http的，但是大家通常都是socks的。所以这个代理步骤就有三个问题:

    - a 创建代理. whatever it works.
     
        最简单的方法```ssh -ND 1234 user@remote_proxy_server```.
        [shadowsocks](https://github.com/shadowsocks)也比较常见。然后就是将socks转换为http代理:

        ```bash
         apt install -y privoxy

         #添加配置
         vi /etc/privoxy/config 
         # 127.0.0.1:1080为本地sock地址
         # 192.168.191.138:8118是要转换的http地址
         forward-socks5 / 127.0.0.1:1234 .
         listen-address 192.168.1.138:1080

         systemctl enable privoxy
         systemctl start privoxy
         #测试下代理是否成功
         curl -x 192.168.138.1:1080 www.google.com
         ```

  - b docker配置代理。

       ```bash
        systemctl enable docker
        mkdir -p /etc/systemd/system/docker.service.d/
        vim /etc/systemd/system/docker.service.d/http-proxy.conf
        [Service]
        Environment="HTTP_PROXY=http://192.168.1.138:1080/" "HTTPS_PROXY=http://192.168.1.138:1080" \
            "NO_PROXY=localhost,127.0.0.1,10.0.0.0/8,192.168.191.138" \

        systemctl daemon-reload;systemctl restart docker
       ```    

  - c 当前执行环境的代理      

       ```bash
        export HTTP_PROXY=http://192.168.1.106:1080/
        export HTTPS_PROXY=http://192.168.1.106:1080/
        export NO_PROXY=localhost,127.0.0.1,10.0.0.0/8,192.168.1.0/24
       ```

- 5 kubeadm配置集群

    ```bash
    #启动
    kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.1.106 --kubernetes-version=v1.10.0
    #任何步骤出错了之后重置
    kubeadm reset

    # 完成后用户配置
    mkdir -p $HOME/.kube
    cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    chown $(id -u):$(id -g) $HOME/.kube/config
    
    # 检查已经启动的服务情况，注意用户不同可能会出现奇怪错误，这时候dns应该还没有ready
    kubectl get pods --all-namespaces

    #其实root很省事的，其他用户自己改掉
    export KUBECONFIG=/etc/kubernetes/admin.conf

    # 安装网络组件，yml文件先check下链接有木有变掉，变的话直接github上flannel里找下
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml

    # 让master也能create pod
    kubectl taint nodes --all node-role.kubernetes.io/master-

    # dashboard启动，默认只能localhost查看,关键参数--accept-hosts
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
    kubectl proxy --address="0.0.0.0"  --port=9090 --accept-hosts='^*$'

    # dashboard url
    http://master-ip:port/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/

    # 看下所有的服务都run起来
    kubectl get pods --all-namespaces -o wide
    
    ```

- 6 完工


### Ref

 - <https://kubernetes.io/docs/getting-started-guides/ubuntu/>       
 - <http://www.winseliu.com/blog/2017/07/30/kubeadm-install-kubenetes-on-centos7/>       
 - <https://blog.alexellis.io/kubernetes-in-10-minutes/>       
 - <https://github.com/kubernetes/dashboard/issues/692>       
 - <https://github.com/kubernetes/kubernetes/issues/48378>       
 - <https://github.com/kubernetes/dashboard/wiki/Access-control>       
 - <https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/>       
 - <https://github.com/kubernetes/dashboard/>    
 - <https://tutorials.ubuntu.com/tutorial/install-kubernetes-with-conjure-up>    
 - <https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#master-isolation>    
 - <https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/>    
 - <https://insights.ubuntu.com/2017/11/13/how-to-deploy-one-or-more-kubernetes-clusters-to-a-single-box>    
