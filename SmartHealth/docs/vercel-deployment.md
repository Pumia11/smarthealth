# Vercel 部署指南

本文档介绍如何将 SmartHealth 项目部署到 Vercel。

## 前置准备

1. **Vercel 账号**：访问 [vercel.com](https://vercel.com) 注册账号
2. **GitHub 仓库**：将项目推送到 GitHub 仓库
3. **Supabase 项目**：确保 Supabase 项目已创建并配置好数据库

## 部署步骤

### 1. 连接 GitHub 仓库

1. 登录 Vercel 控制台
2. 点击 "Add New Project"
3. 选择 "Import Git Repository"
4. 选择你的 SmartHealth GitHub 仓库

### 2. 配置项目设置

#### Root Directory
设置为 `frontend`（Astro 前端项目根目录）

#### Build Command
```bash
npm run build
```

#### Output Directory
```bash
dist
```

### 3. 配置环境变量

在 Vercel 项目设置中添加以下环境变量：

#### 前端环境变量
```
PUBLIC_API_BASE_URL=https://your-project.vercel.app/api
```

#### 后端环境变量
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=production
```

### 4. 部署配置

项目根目录的 `vercel.json` 文件已配置好多项目部署：

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/astro"
    },
    {
      "src": "backend/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

### 5. 部署

点击 "Deploy" 按钮开始部署。Vercel 会自动：

1. 检出代码
2. 安装依赖
3. 构建前端和后端
4. 部署到 Vercel 边缘网络

### 6. 验证部署

部署完成后，你会得到一个 Vercel URL，例如：
```
https://smarthealth-xxx.vercel.app
```

访问以下 URL 验证：

- 前端：`https://smarthealth-xxx.vercel.app`
- API 健康检查：`https://smarthealth-xxx.vercel.app/api/health-check`

## 自定义域名

### 1. 添加域名

1. 在 Vercel 项目设置中，点击 "Domains"
2. 输入你的域名，例如 `smarthealth.yourdomain.com`
3. 点击 "Add"

### 2. 配置 DNS

根据 Vercel 提供的 DNS 记录，在你的域名注册商处添加：

```
A     smarthealth    76.76.21.21
CNAME www.smarthealth    cname.vercel-dns.com
```

### 3. SSL 证书

Vercel 会自动为你的域名配置 SSL 证书。

## 环境变量管理

### 开发环境

在本地开发时，使用 `.env` 文件：

```bash
# frontend/.env
PUBLIC_API_BASE_URL=http://localhost:5000/api

# backend/.env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 生产环境

在 Vercel 控制台的 "Environment Variables" 中配置：

1. 进入项目设置
2. 点击 "Environment Variables"
3. 添加所有必要的环境变量
4. 选择环境（Production, Preview, Development）

## 监控和日志

### 查看部署日志

1. 进入 Vercel 项目
2. 点击 "Deployments"
3. 选择一个部署查看日志

### 查看函数日志

1. 进入 Vercel 项目
2. 点击 "Functions"
3. 查看函数执行日志

### 错误追踪

Vercel 会自动追踪错误，你可以在 "Logs" 标签页查看：

- 构建错误
- 运行时错误
- 超时错误

## 性能优化

### 1. 启用缓存

在 `vercel.json` 中配置缓存规则：

```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 2. 图片优化

Astro 会自动优化图片，确保：

- 使用现代图片格式（WebP, AVIF）
- 响应式图片
- 懒加载

### 3. 代码分割

Astro 默认启用代码分割，确保：

- 按路由分割代码
- 按组件分割代码
- 预加载关键资源

## 故障排除

### 部署失败

1. 检查构建日志
2. 确保所有依赖都在 `package.json` 中
3. 检查环境变量是否正确配置

### API 调用失败

1. 检查 `PUBLIC_API_BASE_URL` 是否正确
2. 确保后端 API 正常运行
3. 检查 CORS 配置

### 数据库连接失败

1. 检查 Supabase URL 和 Key 是否正确
2. 确保 Supabase 项目已启用
3. 检查数据库连接池设置

## 持续部署

### 自动部署

每次推送到 `main` 分支时，Vercel 会自动部署：

- Production 环境：`main` 分支
- Preview 环境：其他分支

### 手动部署

1. 进入 Vercel 项目
2. 点击 "Deployments"
3. 点击 "Redeploy" 按钮

### 回滚部署

1. 进入 Vercel 项目
2. 点击 "Deployments"
3. 找到之前的部署
4. 点击 "..." 菜单
5. 选择 "Promote to Production"

## 成本估算

Vercel 免费套餐包括：

- 100GB 带宽/月
- 100GB 存储空间
- 无限次部署
- 1000 次函数调用/天

对于个人健康管理系统，免费套餐通常足够使用。

## 安全建议

1. **环境变量**：永远不要将敏感信息提交到 Git
2. **API Keys**：定期轮换 API Keys
3. **HTTPS**：Vercel 默认启用 HTTPS
4. **速率限制**：在 API 中实现速率限制
5. **认证**：确保所有 API 端点都有适当的认证

## 下一步

部署完成后：

1. 配置自定义域名
2. 设置监控和告警
3. 配置自动备份
4. 设置 CI/CD 流程
5. 性能监控和优化

## 联系支持

如果遇到问题：

- Vercel 文档：https://vercel.com/docs
- Vercel 社区：https://vercel.com/community
- GitHub Issues：在项目仓库提交 Issue
