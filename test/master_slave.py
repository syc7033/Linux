# Redis的高可用就是为了避免单机不可靠问题
# 并发量

'''
Redis 高可用
主从机构
全量同步
增量同步
'''


# 全量同步
# replication buffer
# repl-backlog-buffer
# master
# 写实复制
'''
3.根据参数判断是否能够进行全量同步
    满足什么条件能进行全量同步？
        a.传过来的replid必须是我master的id
            如果不是主结点的id说明之前没进行过全量同步，必须先进行一次全量同步
        b.offset偏移量必须在replication buffer里面
            网络中断后会向replication buffer中写
    反之则进行增量同步

4.进行全量同步，返回master的replid和offset给slave

6.执行bgsave命令(不会阻塞主进程)，生成一个RDB文件(快照方式)
    不会阻塞master说明他是异步的方式，他会产生问题，这生成RDB文件的时候，master可能会传输写命令

7.传输RDB文件

9.记录生成RDB文件和传出RDB文件过程中的写操作命令
    (replication buffer缓冲区的内存不足会导致全量同步的失败，会重新进行全量同步)

10.补发新的写操作命令
'''

# slave
'''
1.执行replicaof命令
    参数 ip port (分别是master的ip和端口号)
    slaveRedis去建立与masterRedis之间的连接
    
2.执行psync命令
    参数 replid offset
    请求同步

5.保存master信息

8.清空本地数据，加载RDB文件

11.接收新的写操作命令
'''


# 1.建立主从结点之间的连接，从节点执行连接指令传主结点的ip和端口号
# 2.从节点向主节点发出同步请求，会传递replid 和 offset
# 3.主节点进行判断，如果replid是主节点的id并且offset量在replication buffer缓冲区中 则进行全量同步 反之则进行增量同步
# 4.进行全量同步，返回主节点的id和偏移量
# 5.保存master的信息
# 6.执行bgsave指令，他是非阻塞的命令，异步，会生成一个RDB文件
# 7.传输这个RDB文件
# 8.由于是非阻塞操作，生成和传输该RDB文件的时候可能会有写命令执行，该写命令保存在赋值缓冲区中
# 10.补发写操作命令
# 11.接收该命令



# 哨兵

'''
哨兵有多个，监控主节点
哨兵的三个阶段

监控
    ping命令
        看主节点是否有响应，如果没有响应，哨兵会标记为主观下线，然后回询问其他的哨兵，该主结点是否网络不好
        如果另外几个哨兵也判断为主管下线，该结点回标记为客观下线
选主
    故障转移的哨兵
    slaveof no one 
    ip port
'''
# 持久化 RDB和AOF文件