# 虚拟3D手部（MediaPipe+OpenCV+Unity3D）
    1. 把3D文件使用unity打开修改脚本的UDP端口监听
    2. 运行py文件，serverAddressPort = ("127.0.0.1", 5052)后面端口可自定义，需与unity一致保证数据传输
    3. 打开3DHand.exe

# 常见错误
    1. 3D手部模型线与点分离
        把3D把点与线的坐标恢复y轴的中心点，或者重新下载项目

    2. c#脚本报错，提示端口类错误
        在cmd中使用命令找出端口对应的进程号，netstat -nao | findstr “8080” 查询8080端口
        查杀此进程，其中16900是您的任务进程 taskkill /pid 16900 -f
