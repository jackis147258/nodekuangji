import http.client
import json

conn = http.client.HTTPSConnection("www.youdao.love")
payload = json.dumps("pageSize=50&pageNum=1&profit=0&time=43200&platform=55,26,66,74,184,110&moveType=15,4,22,3,0,20,17,23,1,24,18,21,12,34,39,45,36")
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'www.youdao.love',
   'Connection': 'keep-alive'
}
conn.request("POST", "/app1/htmlInfo/", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))





 




server
{
    listen 80;
    server_name  www.youdao.loved;
    index index.html index.htm default.htm default.html;
    root /www/wwwroot/ticaivs/ticai;

    #SSL-START SSL相关配置
    #error_page 404/404.html;
    
    #SSL-END

    #ERROR-PAGE-START  错误页相关配置
    #error_page 404 /404.html;
    #error_page 502 /502.html;
    #ERROR-PAGE-END


    #REWRITE-START 伪静态相关配置
   
    include /www/server/panel/vhost/rewrite/www.youdao.love.conf;

    #REWRITE-END

    #禁止访问的文件或目录
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.svn|\.project|LICENSE|README.md|package.json|package-lock.json|\.env) {
        return 404;
    }

    #一键申请SSL证书验证目录相关设置
    location /.well-known/ {
        root /www/wwwroot/java_node_ssl;
    }

    #禁止在证书验证目录放入敏感文件
    if ( $uri ~ "^/\.well-known/.*\.(php|jsp|py|js|css|lua|ts|go|zip|tar\.gz|rar|7z|sql|bak)$" ) {
        return 403;
    }

    # HTTP反向代理相关配置开始 >>>
    location ~ /purge(/.*) {
        proxy_cache_purge cache_one 127.0.0.1$request_uri$is_args$args;
    }

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host 127.0.0.1:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header REMOTE-HOST $remote_addr;
        add_header X-Cache $upstream_cache_status;
        proxy_set_header X-Host $host:$server_port;
        proxy_set_header X-Scheme $scheme;
        proxy_connect_timeout 30s;
        proxy_read_timeout 86400s;
        proxy_send_timeout 30s;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    # HTTP反向代理相关配置结束 <<<

    access_log  /www/wwwroot/ticaivs/ticai/ticai2.log;
    error_log  /www/wwwroot/ticaivs/ticai/ticai2.error.log;
}