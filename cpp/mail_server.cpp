
// #include "TcpServer.h"
// #include <iostream>
// #include <string>

// #include <hiredis/hiredis.h>
// #include <hiredis/async.h>
// #include <adapters/libhv.h>

// using namespace hv;

// #include "protorpc.h"
// #include "router.h"
// #include "handler/handler.h"
// #include "handler/calc.h"
// #include "handler/login.h"
// #include "include/hv/generated/general.pb.h"
// #include "time.h"

// // valgrind --leak-check=full --show-leak-kinds=all
// class ProtobufRAII {
// public:
//     ProtobufRAII() {
//     }
//     ~ProtobufRAII() {
//         google::protobuf::ShutdownProtobufLibrary();
//     }
// };
// static ProtobufRAII s_protobuf;

// void getCallback(redisAsyncContext *c, void *r, void *privdata);
// void debugCallback(redisAsyncContext *c, void *r, void *privdata);
// void connectCallback(const redisAsyncContext *c, int status);
// void disconnectCallback(const redisAsyncContext *c, int status);

// void send_mail(redisAsyncContext *c, Mail mail)
// {
//     std::vector<long long> useridlist;
//     for (int i = 0; i < mail.userid_size(); i++)
//     {
//         // 全服邮件
//         // std::cout << "userid" << i << ": " << mail.userid(i) << std::endl;
//         useridlist.push_back(mail.userid(i));
//     }
//     std::string title = mail.title();
//     std::string context = mail.context();
//     int type = mail.type();
//     std::string attach = mail.attach();
//     std::string buttontext = mail.buttontext();
//     int hasattach = mail.hasattach();
//     int getattach = mail.getattach();

//     std::string userid;
//     std::string mailid;
//     std::string listKey;

//     for (int i = 0; i < mail.userid_size(); i++)
//     {
//         userid = std::to_string(mail.userid(i));
//         mailid = userid + '_' + std::to_string(time(NULL));

//         // redisReply *reply;
//         size_t argvlen[16];
//         const char *argv[16];

//         std::string KEY_MAIL_LIST = "KEY_MAIL_LIST_" + userid;

//         argv[0] = "RPUSH";
//         argvlen[0] = strlen("RPUSH");
//         argv[1] = KEY_MAIL_LIST.c_str();
//         argvlen[1] = strlen(KEY_MAIL_LIST.c_str());
//         argv[2] = mailid.c_str();
//         argvlen[2] = strlen(mailid.c_str());

//         // 执行命令
//         redisAsyncCommandArgv(c, NULL, NULL, 3, argv, argvlen);

//         const char *mail_title = title.c_str();
//         const char *mail_type = std::to_string(type).c_str();
//         const char *mail_context = context.c_str();
//         const char *mail_attach = attach.c_str();
//         const char *mail_buttontext = buttontext.c_str();
//         const char *mail_hasattach = std::to_string(hasattach).c_str();
//         const char *mail_getattach = std::to_string(getattach).c_str();

//         // redisReply *reply;
//         memset(argvlen, 0, sizeof(argvlen));
//         memset(argv, 0, sizeof(argv));

//         std::string KEY_MAILDETAIL = "KEY_MAIL_DETAIL_" + mailid;
//         argv[0] = "HMSET";
//         argvlen[0] = strlen("HMSET");
//         argv[1] = KEY_MAILDETAIL.c_str();
//         argvlen[1] = strlen(KEY_MAILDETAIL.c_str());
//         argv[2] = "title";
//         argvlen[2] = strlen("title");
//         argv[3] = mail_title;
//         argvlen[3] = strlen(mail_title);
//         argv[4] = "context";
//         argvlen[4] = strlen("context");
//         argv[5] = mail_context;
//         argvlen[5] = strlen(mail_context);
//         argv[6] = "type";
//         argvlen[6] = strlen("type");
//         argv[7] = mail_type;
//         argvlen[7] = strlen(mail_type);
//         argv[8] = "attach";
//         argvlen[8] = strlen("attach");
//         argv[9] = mail_attach;
//         argvlen[9] = strlen(mail_attach);
//         argv[10] = "buttontext";
//         argvlen[10] = strlen("buttontext");
//         argv[11] = mail_buttontext;
//         argvlen[11] = strlen(mail_buttontext);
//         argv[12] = "hasattach";
//         argvlen[12] = strlen("hasattach");
//         argv[13] = mail_hasattach;
//         argvlen[13] = strlen(mail_hasattach);
//         argv[14] = "getattach";
//         argvlen[14] = strlen("getattach");
//         argv[15] = mail_getattach;
//         argvlen[15] = strlen(mail_getattach);

//         // 执行命令
//         redisAsyncCommandArgv(c, NULL, NULL, 16, argv, argvlen);
//     }
// }

// void handle_mail(Mail mail) {
//     #ifndef _WIN32
//         signal(SIGPIPE, SIG_IGN);
//     #endif

//     //创建redis异步连接
//     redisAsyncContext *c = redisAsyncConnect("127.0.0.1", 6379);

  
//     if (c == NULL || c->err) {
//         if (c) {
//             printf("Error: %s\n", c->errstr);
//             // handle error
//             return;
//         } else {
//             printf("Can't allocate redis context\n");
//             return;
//         }
//     }

//     hloop_t* loop = hloop_new(HLOOP_FLAG_QUIT_WHEN_NO_ACTIVE_EVENTS);
//     redisLibhvAttach(c, loop);

//     //为Redis连接设置了超时时间
//     redisAsyncSetTimeout(c, (struct timeval){.tv_sec = 0, .tv_usec = 10000});

//     redisAsyncSetConnectCallback(c,connectCallback);

//     redisAsyncSetDisconnectCallback(c,disconnectCallback);

//     //认证
//     redisAsyncCommand(c, NULL, NULL, "auth %s", "123456");
//     redisAsyncCommand(c, getCallback, (char*)"end-1", "GET key");
//     send_mail(c, mail);
//     hloop_run(loop);
//     hloop_free(&loop);
// }

// class ProtoRpcServer : public TcpServer {
// public:
//     ProtoRpcServer() : TcpServer()
//     {
//         onConnection = [](const SocketChannelPtr& channel) {
//             std::string peeraddr = channel->peeraddr();
//             if (channel->isConnected()) {
//                 printf("%s connected! connfd=%d\n", peeraddr.c_str(), channel->fd());
//             } else {
//                 printf("%s disconnected! connfd=%d\n", peeraddr.c_str(), channel->fd());
//             }
//         };
//         onMessage = handleMessage;
//         // init protorpc_unpack_setting
//         unpack_setting_t protorpc_unpack_setting;
//         memset(&protorpc_unpack_setting, 0, sizeof(unpack_setting_t));
//         protorpc_unpack_setting.mode = UNPACK_BY_LENGTH_FIELD;
//         protorpc_unpack_setting.package_max_length = DEFAULT_PACKAGE_MAX_LENGTH;
//         protorpc_unpack_setting.body_offset = PROTORPC_HEAD_LENGTH;
//         protorpc_unpack_setting.length_field_offset = PROTORPC_HEAD_LENGTH_FIELD_OFFSET;
//         protorpc_unpack_setting.length_field_bytes = PROTORPC_HEAD_LENGTH_FIELD_BYTES;
//         protorpc_unpack_setting.length_field_coding = ENCODE_BY_BIG_ENDIAN;
//         setUnpack(&protorpc_unpack_setting);
//     }

//     int listen(int port) { return createsocket(port); }

// private:
//     static void handleMessage(const SocketChannelPtr& channel, Buffer* buf) {
//         protorpc_message msg;
//         printf("%s", (char*)buf->data());
//         printf("%ld", buf->size());
//         memset(&msg, 0, sizeof(msg));
//         int packlen = protorpc_unpack(&msg, buf->data(), buf->size());
//         if (packlen < 0) {
//             printf("protorpc_unpack failed!\n");
//             return;
//         }
//         assert(packlen == buf->size());
//         if (protorpc_head_check(&msg.head) != 0) {
//             printf("protorpc_head_check failed!\n");
//             return;
//         }

//         Mail mail;
//         printf("head.length = %d", msg.head.length);
//         if(mail.ParseFromArray(msg.body, msg.head.length))
//         {
//             handle_mail(mail);
//         }
//     }
// };

// void getCallback(redisAsyncContext *c, void *r, void *privdata) {
//     redisReply *reply = (redisReply*)r;
//     if (reply == NULL) return;
//     //printf("argv[%s]: %s\n", (char*)privdata, reply->str);

//     /* Disconnect after receiving the reply to GET */
//     redisAsyncDisconnect(c);
// }

// void debugCallback(redisAsyncContext *c, void *r, void *privdata) {
//     (void)privdata;
//     redisReply *reply = (redisReply*)r;

//     if (reply == NULL) {
//         printf("`DEBUG SLEEP` error: %s\n", c->errstr ? c->errstr : "unknown error");
//         return;
//     }

//     redisAsyncDisconnect(c);
// }

// void connectCallback(const redisAsyncContext *c, int status) {
//     if (status != REDIS_OK) {
//         printf("Error: %s\n", c->errstr);
//         return;
//     }
//     printf("Connected...\n");
// }

// void disconnectCallback(const redisAsyncContext *c, int status) {
//     if (status != REDIS_OK) {
//         printf("Error: %s\n", c->errstr);
//         return;
//     }
//     printf("Disconnected...\n");
// }

// int main(int argc, char** argv) {
//     if (argc < 2) {
//         printf("Usage: %s port\n", argv[0]);
//         return -10;
//     }
//     int port = atoi(argv[1]);

//     ProtoRpcServer srv;
//     int listenfd = srv.listen(port);
//     if (listenfd < 0) {
//         return -20;
//     }
//     printf("protorpc_server listen on port %d, listenfd=%d ...\n", port, listenfd);
//     srv.setThreadNum(4);
//     srv.start();
    
//     while (1) hv_sleep(1);
//     return 0;
// }
