#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SER_IP "192.168.22.136"
#define SER_PORT 8001


int main(int argc, char* argv[]){
    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    printf("lfd = %d\n", lfd);
    
    struct sockaddr_in serAddr;
    serAddr.sin_family = AF_INET;
    serAddr.sin_port = htons(SER_PORT);
    serAddr.sin_addr.s_addr = inet_pton(AF_INET, SER_IP, NULL);

    bind(lfd, (struct sockaddr*)&serAddr, sizeof(serAddr));
    
    listen(lfd, 64);

    int cfd = accept(lfd, NULL, NULL);
    printf("cfd = %d\n", cfd);

    int readLen = 0;
    char buf[1024] = {'\0'};

    while(1){
        readLen = read(cfd, buf, sizeof(buf));
        if(readLen == 0){
            close(cfd);
            return 0;
        }
        write(STDOUT_FILENO, buf, readLen);
    }

    return 0;
}