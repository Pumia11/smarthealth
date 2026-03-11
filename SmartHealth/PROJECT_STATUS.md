# SmartHealth 项目状态文档

> 最后更新：2026-03-11
> 项目状态：暂停开发

---

## 📋 项目概述

**SmartHealth** 是一个个人健康管理系统，采用 Pixel Art 像素风格UI设计，集成AI健康分析功能。

### 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Astro 4.x + React 18 + Tailwind CSS |
| 后端 | Flask (Python) |
| 数据库 | Supabase (PostgreSQL) |
| AI服务 | MiniMax API |
| 部署 | Vercel (前端+后端) |
| 字体 | Fusion Pixel Font |

### 项目地址

- **GitHub**: https://github.com/Pumia11/smarthealth
- **前端部署**: Vercel (已部署)
- **后端部署**: https://smarthealth-backend-six.vercel.app/

---

## ✅ 已完成工作

### 1. 前端开发

- [x] Astro项目初始化
- [x] Pixel Art UI设计系统
- [x] Fusion Pixel字体集成
- [x] 页面开发：
  - [x] 首页 (`/`)
  - [x] 登录页 (`/login`)
  - [x] 注册页 (`/register`)
  - [x] 健康记录页 (`/health`)
  - [x] 饮食记录页 (`/diet`)
  - [x] 运动记录页 (`/exercise`)
  - [x] AI分析页 (`/ai`)
- [x] 响应式布局
- [x] Zustand状态管理
- [x] API请求封装

### 2. 后端开发

- [x] Flask项目初始化
- [x] Vercel Serverless部署配置
- [x] API端点开发：
  - [x] `/api/auth/register` - 用户注册
  - [x] `/api/auth/login` - 用户登录
  - [x] `/api/auth/me` - 用户资料
  - [x] `/api/health/indicators` - 健康指标
  - [x] `/api/health/records` - 健康记录
  - [x] `/api/diet/records` - 饮食记录
  - [x] `/api/exercise/records` - 运动记录
  - [x] `/api/ai/analyze` - AI健康分析
- [x] JWT认证集成
- [x] Supabase数据库连接
- [x] MiniMax AI集成

### 3. 数据库设计

- [x] Supabase项目创建
- [x] 数据库表结构设计（19张表）
- [x] Row Level Security配置
- [x] 默认数据插入

### 4. 部署配置

- [x] 前端Vercel部署
- [x] 后端Vercel部署
- [x] GitHub仓库配置
- [x] 环境变量配置

---

## 🔄 当前状态

### 前端
- **状态**: ✅ 已部署
- **URL**: Vercel分配的域名
- **构建**: 正常

### 后端
- **状态**: ✅ 已部署
- **URL**: https://smarthealth-backend-six.vercel.app/
- **健康检查**: 正常
- **API**: 所有端点可用

### 数据库
- **状态**: ✅ 已配置
- **Supabase**: 已创建表结构

---

## 📝 待完成任务

### 高优先级

- [ ] **测试注册登录功能** - 验证Supabase Auth是否正常工作
- [ ] **配置Supabase Email设置** - 可能需要关闭邮箱验证用于测试
- [ ] **前端连接后端测试** - 验证API调用是否正常

### 中优先级

- [ ] **完善健康记录功能** - 添加记录的CRUD操作
- [ ] **完善饮食记录功能** - 食物库数据填充
- [ ] **完善运动记录功能** - 运动库数据填充
- [ ] **AI分析功能优化** - 完善MiniMax调用

### 低优先级

- [ ] **文章系统开发** - 健康文章展示
- [ ] **食谱功能开发** - 健康食谱推荐
- [ ] **提醒功能开发** - 健康提醒任务
- [ ] **数据可视化** - 图表展示健康趋势

---

## 🔧 环境变量配置

### 后端 (Vercel)

```
SUPABASE_URL=你的Supabase项目URL
SUPABASE_KEY=你的Supabase anon key
MINIMAX_API_KEY=sk-api-MRoTbTnLCGt8jyKCZRNBKF5oMGBR8H59eKewTE3VWx5gWSvtk6QyaNepxzmXUhOqX_Z3iRtcLwkPM1RoOn3m9aNOeSCowTl4_FDMiPaI4a66fYv_shCjs0I
MINIMAX_GROUP_ID=2028443032323367699
SECRET_KEY=smarthealth-pixel-art-secret-2024
JWT_SECRET_KEY=jwt-secret-key-smarthealth
```

### 前端 (Vercel)

```
PUBLIC_API_BASE_URL=https://smarthealth-backend-six.vercel.app/api
```

---

## 📁 项目结构

```
SmartHealth/
├── frontend/                    # Astro前端项目
│   ├── src/
│   │   ├── components/         # React组件
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── layouts/            # 页面布局
│   │   ├── pages/              # 页面路由
│   │   │   ├── index.astro     # 首页
│   │   │   ├── login.astro     # 登录
│   │   │   ├── register.astro  # 注册
│   │   │   ├── health/         # 健康记录
│   │   │   ├── diet/           # 饮食记录
│   │   │   ├── exercise/       # 运动记录
│   │   │   └── ai/             # AI分析
│   │   ├── stores/             # Zustand状态
│   │   ├── styles/             # 全局样式
│   │   └── utils/              # 工具函数
│   ├── public/
│   │   └── fonts/              # Fusion Pixel字体
│   ├── package.json
│   ├── astro.config.mjs
│   └── tailwind.config.mjs
│
├── backend/                     # Flask后端项目
│   ├── api/
│   │   └── index.py            # Vercel入口点
│   ├── app/
│   │   ├── routes/             # API路由
│   │   ├── services/           # 服务层
│   │   └── utils/              # 工具函数
│   ├── requirements.txt
│   └── vercel.json
│
├── docs/
│   └── supabase-schema.sql     # 数据库结构
│
├── vercel.json                  # 前端部署配置
└── README.md
```

---

## 🚀 重启开发指南

### 1. 克隆项目

```bash
git clone https://github.com/Pumia11/smarthealth.git
cd smarthealth
```

### 2. 前端开发

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:4321
```

### 3. 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 创建 .env 文件并配置环境变量
python -c "from api.index import app; app.run(debug=True)"
# 访问 http://localhost:5000
```

### 4. 检查部署状态

- 前端: Vercel Dashboard
- 后端: https://smarthealth-backend-six.vercel.app/
- 数据库: Supabase Dashboard

---

## 🐛 已知问题

1. **Vercel Python部署** - 需要简化配置，不能使用复杂的模块导入
2. **Supabase Auth** - 可能需要配置邮箱验证设置
3. **CORS** - 已配置允许所有来源，生产环境需要限制

---

## 📚 参考文档

- [Astro文档](https://docs.astro.build/)
- [Flask文档](https://flask.palletsprojects.com/)
- [Supabase文档](https://supabase.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [MiniMax API](https://www.minimaxi.com/)
- [Fusion Pixel Font](https://github.com/TakWolf/fusion-pixel-font)

---

## 📞 联系方式

- GitHub: https://github.com/Pumia11/smarthealth
