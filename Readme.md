# ClubMan

## 简介
ClubMan 是一个用于俱乐部管理的Web应用程序，旨在帮助俱乐部管理员轻松管理会员信息、活动安排、费用收缴等。

## 技术栈
- **前端**: Vue.js, TypeScript
- **后端**: Python (Flask)
- **数据库**: Mysql

## 安装步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/your-repo/ClubMan.git
   cd ClubMan
   ```

2. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

3. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **导入数据库Mysql**
   ```bash
   python backend/init_db.py
   ```

## 使用方法
1. **启动前端**
   ```bash
   cd frontend
   npm run serve
   ```

2. **启动后端**
   ```bash
   cd backend
   python app.py
   ```

3. **访问应用**
   打开浏览器，访问 `http://localhost:8080`。

## 贡献指南
欢迎任何形式的贡献！请参考以下步骤：
1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证
本项目采用 MIT 许可证。请参阅 [LICENSE](LICENSE.txt) 文件获取更多信息。
