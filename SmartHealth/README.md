# SmartHealth - 个人健康管理系统

一个基于 **Python + Astro + Flask** 的个人健康管理系统，采用 **Pixel Art** 像素风格UI设计。

## 🎮 项目特点

- **Pixel Art 风格**：独特的像素风格UI设计，使用 Fusion Pixel 字体
- **多端支持**：支持 Web 端访问，响应式设计
- **AI 健康分析**：集成 DeepSeek AI，提供智能健康分析
- **完整功能**：健康指标管理、饮食记录、运动追踪、健康知识

## 🛠️ 技术栈

### 前端
- **Astro** - 现代化静态站点生成器
- **React** - UI 组件库
- **Tailwind CSS** - 原子化 CSS 框架
- **Zustand** - 轻量级状态管理
- **TypeScript** - 类型安全

### 后端
- **Flask** - Python Web 框架
- **Supabase** - 后端即服务（数据库、认证）
- **JWT** - 身份认证
- **Python 3.11+**

### 部署
- **Vercel** - 前端部署平台
- **Supabase** - 数据库和认证服务

## 📦 项目结构

```
SmartHealth/
├── frontend/                 # Astro 前端项目
│   ├── src/
│   │   ├── components/      # React 组件
│   │   ├── layouts/         # 页面布局
│   │   ├── pages/           # 页面路由
│   │   ├── stores/          # 状态管理
│   │   ├── styles/          # 全局样式
│   │   └── utils/           # 工具函数
│   ├── public/              # 静态资源
│   └── package.json
│
├── backend/                  # Flask 后端项目
│   ├── app/
│   │   ├── routes/          # API 路由
│   │   ├── services/        # 业务逻辑
│   │   ├── models/          # 数据模型
│   │   └── utils/           # 工具函数
│   ├── config.py            # 配置文件
│   ├── app.py               # 应用入口
│   └── requirements.txt     # Python 依赖
│
└── docs/                     # 项目文档
```

## 🚀 快速开始

### 前置要求

- Node.js 18+
- Python 3.11+
- Supabase 账号
- Vercel 账号（可选，用于部署）

### 1. 克隆项目

```bash
git clone <repository-url>
cd SmartHealth
```

### 2. 配置 Supabase

1. 创建 [Supabase](https://supabase.com) 项目
2. 运行 `docs/supabase-schema.sql` 创建数据表
3. 获取项目 URL 和 API Key

### 3. 配置后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 Supabase 配置

# 启动服务
python app.py
```

### 4. 配置前端

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API 地址

# 启动开发服务器
npm run dev
```

### 5. 访问应用

- 前端：http://localhost:4321
- 后端 API：http://localhost:5000

## 🎨 Pixel Art 设计系统

### 颜色方案

```css
--pixel-bg: #1a1c2c        /* 背景色 */
--pixel-surface: #262b44   /* 表面色 */
--pixel-primary: #5d275d   /* 主色 */
--pixel-secondary: #b13e53 /* 辅助色 */
--pixel-accent: #ef7d57    /* 强调色 */
--pixel-success: #3b5dc9   /* 成功色 */
--pixel-warning: #ffcd75   /* 警告色 */
--pixel-text: #f4f4f4      /* 文字色 */
--pixel-muted: #5a6988     /* 次要文字 */
--pixel-border: #3a4466    /* 边框色 */
```

### 字体

项目使用 **Fusion Pixel** 字体，请确保已安装该字体。

## 📚 API 文档

### 认证接口

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户
- `PUT /api/auth/me` - 更新用户信息

### 健康指标接口

- `GET /api/health/indicators` - 获取健康指标列表
- `POST /api/health/indicators` - 创建健康指标
- `GET /api/health/records` - 获取健康记录
- `POST /api/health/records` - 创建健康记录
- `GET /api/health/stats` - 获取健康统计

### 饮食管理接口

- `GET /api/diet/foods` - 获取食物列表
- `GET /api/diet/food-types` - 获取食物分类
- `GET /api/diet/records` - 获取饮食记录
- `POST /api/diet/records` - 创建饮食记录
- `GET /api/diet/stats/daily` - 获取每日统计

### 运动管理接口

- `GET /api/exercise/exercises` - 获取运动列表
- `GET /api/exercise/exercise-types` - 获取运动分类
- `GET /api/exercise/records` - 获取运动记录
- `POST /api/exercise/records` - 创建运动记录
- `GET /api/exercise/stats/daily` - 获取每日统计

### AI 分析接口

- `POST /api/ai/analyze` - 执行健康分析
- `GET /api/ai/reports` - 获取分析报告列表
- `GET /api/ai/reports/:id` - 获取分析报告详情

## 🚢 部署

### Vercel 部署（前端）

1. 连接 GitHub 仓库到 Vercel
2. 设置 Root Directory 为 `frontend`
3. 配置环境变量
4. 部署

### 后端部署

后端可以部署到：
- **Vercel** - 使用 Vercel 的 Python 运行时
- **Railway** - 支持 Python 应用
- **Render** - 免费 Python 托管
- **自建服务器** - 使用 Gunicorn + Nginx

## 📝 开发计划

- [ ] 微信小程序端
- [ ] 健康数据可视化图表
- [ ] 更多 AI 分析功能
- [ ] 健康提醒推送
- [ ] 数据导入导出
- [ ] 多语言支持

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
