# 卡密管理系统

一个简单但功能完整的卡密（激活码）管理系统，基于Python Flask开发，支持卡密的生成、验证和管理。

## 功能特点

- 📝 管理员登录系统
- 🎫 生成指定有效期的卡密
- ✅ 验证卡密的有效性
- 📊 查看所有卡密列表（分页显示）
- 👤 管理员账户信息修改
- 🔒 JWT Token加密验证

## 技术栈

- Backend:
  - Python 3.x
  - Flask (Web框架)
  - SQLite3 (数据库)
  - PyJWT (JWT token处理)
  
- Frontend:
  - HTML5
  - Bootstrap 5.3
  - JavaScript (原生)

## 快速开始

### 1. 环境要求

- Python 3.x
- pip (Python包管理器)

### 2. 安装依赖

```bash
pip install flask pyjwt
```

### 3. 运行应用

```bash
python app.py
```

应用将在 http://localhost:9840 启动

### 4. 默认管理员账户

- 用户名：yuer
- 密码：yuerpass

## 系统功能说明

### 卡密生成
- 管理员可以生成指定有效期的卡密
- 卡密基于JWT加密生成，包含创建时间和过期时间信息

### 卡密验证
- 支持实时验证卡密的有效性
- 显示卡密的创建时间和状态

### 卡密管理
- 分页显示所有已生成的卡密
- 包含卡密ID、完整卡密内容和创建时间

### 安全特性
- 使用Session进行登录状态管理
- 密码采用SHA256加密存储
- JWT token确保卡密的安全性和有效期控制

## 文件结构

- `app.py` - 主应用程序文件，包含所有API路由
- `db.py` - 数据库操作相关函数
- `jwt_util.py` - JWT token生成和验证工具
- `index.html` - 前端界面
- `database.db` - SQLite数据库文件（自动生成）

## 注意事项

1. 首次运行时会自动创建数据库和默认管理员账户
2. 生产环境部署时请修改以下安全配置：
   - `app.secret_key`
   - `jwt_util.py` 中的 `SECRET_KEY`
   - 默认管理员账户的用户名和密码

## 开发者说明

- 本系统使用SQLite作为数据库，无需额外配置数据库服务
- 前端使用Bootstrap实现响应式设计
- API接口采用RESTful设计风格