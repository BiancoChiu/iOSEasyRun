# iOSEasyRun

本项目基于 [iOSRealRun-cli-17](https://github.com/iOSRealRun/iOSRealRun-cli-17) 修改而来，并更新了依赖的 [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)。

测试环境：
- 操作系统：MacOS
- Python版本：3.13
- iOS版本：18.3.1

## 用法简介

### 前置条件

1. 系统是 `Windows` 或 `MacOS`（Windows暂未测试，出现问题请提issue）
2. iPhone 或 iPad 系统版本大于等于 18（也许17的一些后期版本也可以用，未经测试）
3. Windows 需要安装 iTunes
4. 已安装 `Python3` 和 `pip3`
5. **重要**: 只能有一台 iPhone 或 iPad 连接到电脑，否则会出问题

### 步骤

1. 安装依赖（建议使用虚拟环境）  
    ```shell
    pip3 install -r requirements.txt
    ```
    如果 `pip3` 无法安装，请使用 `pip` 替代  
    如果提示没有需要的版本，请尝试不适用国内源  
2. 修改配置和路线文件，修改速度和圈数
    - 路线文件：打开[坐标拾取网站](https://fakerun.myth.cx/)，画一圈，首尾尽量接近，之后将路线内容粘贴到`route.txt`
    - 速度与圈数：修改`config.yaml`中的速度和圈数
3. 将设备连接到电脑，解锁，如果请求信任的提示框，请点击信任
4. 打开终端（cmd 或 PowerShell），执行以下命令获取DDI（仅首次使用需运行）
    ```shell
    pymobiledevice3 mounter auto-mount
    ```
5. 运行gpx.py生成路径文件（仅首次使用需运行）
    ```shell
    python gpx.py
    ```
6. Windows **以管理员身份** 打开终端（cmd 或 PowerShell），先进入项目目录，然后执行以下命令 
    ```shell
    python main.py
    ```
    MacOS 打开终端，先进入项目目录，然后执行以下命令  
    ```shell
    sudo python3 main.py
    ```

7. (optional) 如果出现报错可以尝试手动启动
开启两个终端窗口，第一个窗口运行以下命令之一（需要管理员权限），根据你的不同版本可能需要的命令不同
    ```shell
    pymobiledevice3 lockdown start-tunnel
    pymobiledevice3 remote start-tunnel
    pymobiledevice3 remote tunneld
    ```
运行后会出现一些rsd相关信息如
    ```
    RSD Address: fd25:5d47:c482::1
    RSD Port: 50594
    Use the follow connection option:
    --rsd fd25:5d47:c482::1 50594
    # or
    2025-02-25 10:58:59 Biancos-MacBook-Pro.local pymobiledevice3.tunneld.server[22550] INFO [start-tunnel-task-usbmux-00008110-001E154111A2801E-USB] Created tunnel --rsd fd48:b177:8176::1 50597
    ```

接下来在第二个终端窗口运行以下命令（无需管理员权限），如`pymobiledevice3 developer dvt simulate-location play track.gpx --rsd fd48:b177:8176::1 50597`
    ```shell
    pymobiledevice3 developer dvt simulate-location play track.gpx --rsd <your_RSD_address> <your_RSD_port>
    ```

- 按照提示操作，如果一直说没有设备连接，Windows请确保 iTunes 已安装（可能需要打开），重新运行程序，在第3步时请确保设备已连接，解锁并信任
- 结束请务必使用 `Ctrl + C` 终止程序，否则可能无法恢复定位
- 如果定位未恢复，可以重启手机解决
