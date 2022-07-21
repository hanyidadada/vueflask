# vueflask
如何运行
## Flask后端
### 1.创建python3虚拟环境
    python3 -m venv .venv
### 2.进入虚拟环境
    source .venv/bin/activate
### 3.下载flask依赖
    pip install flask
    pip install flask_cors
    pip install pillow
    pip install tk
    sudo apt install python3-tk
### 4.开始运行
    python3 -m flask run
若本步骤仍然报错，则继续使用pip安装缺少的依赖包
## VUE前端
    npm install
    npm run dev