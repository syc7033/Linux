#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SER_IP "192.168.22.136"
#define SER_PROT 8001

int main(){
    int cfd = socket(AF_INET, SOCK_STREAM, 0);
    printf("cfd = %d\n", cfd);

    /*
    客户端的socket可以不显示绑定地址，会隐式绑定一个端口号
    通常来讲不绑定会更好一些
    因为当客户端主动断开连接，最后会进入timewait状态会持续2MSL，这个时候如果是显示绑定，那么客户端要想再
    建立与服务器之间的连接就会出错，因为timewait进程占用了显示绑定的端口，但是如果是隐式绑定，则会重新分配一个端口
    */
    struct sockaddr_in serAddr;
    serAddr.sin_family = AF_INET;
    serAddr.sin_port = htons(SER_PROT);
    serAddr.sin_addr.s_addr = inet_pton(AF_INET, SER_IP, NULL);

    int ret = connect(lfd, (struct sockaddr*)&serAddr, sizeof(serAddr));
    printf("connect ret = %d\n", ret);

    while(1){
        write(cfd, "hello\n", 5);
        sleep(1);
    }
    return 0;
}