生成项目
mvn -B archetype:generate   -DarchetypeGroupId=org.apache.maven.archetypes   -DgroupId=com.duozhun.app   -DartifactId=dmp_crowd

导入Idea

修改pomjunit test版本为4.4，取消缓存，重启IDEA

下载sdk
打开idea，在代码一级目录下新建lib文件夹
在idea中，Ctrl + Shift + Alt + S
libraries 添加lib目录，应用，确定，取消缓存，重启IDEA

pom中添加loggin的依赖
<!-- https://mvnrepository.com/artifact/commons-logging/commons-logging -->
<dependency>
    <groupId>commons-logging</groupId>
    <artifactId>commons-logging</artifactId>
    <version>1.1.1</version>
</dependency>


添加下面代码

String url = "http://gw.api.taobao.com/router/rest";
String appkey = "23360075";
String secret = "50272e1da15cf5b1b5885ec81ca73ae6";
String sessionKey = "62003061abdef7ZZcecb3e5b600d818b55b13d132a5d626479218086";
TaobaoClient client = new DefaultTaobaoClient(url, appkey, secret);
DmpTagsGetRequest req = new DmpTagsGetRequest();
DmpTagsGetResponse rsp = client.execute(req, sessionKey);
System.out.println(rsp.getBody());

自动导入包，改掉小bug。

打开沙箱测试环境
http://open.taobao.com/apitools/apiTools.htm?spm=a219a.7395905.0.0.XnM9l7&catId=20662&apiId=24379&apiName=taobao.zuanshi.adzones.get&scopeId=11606

测试session key获取过程


http://www.ibm.com/developerworks/cn/java/j-lo-tomcat1/

http://www.ibm.com/developerworks/cn/java/j-lo-servlet/

