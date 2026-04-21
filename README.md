# 文本展示软件

一款基于 React + TypeScript + Framer Motion 开发的高美感文本展示工具。

## 功能特点

1. **文本预处理**：自动按段落和标点符号（。/ . / ? / !）切分句子。
2. **双模式引擎**：
   - **随机模式**：使用 Fisher-Yates 洗牌算法，保证句子不重复展示，全播完后重置。
   - **交互模式**：提供上一条、暂停/继续、下一条控制。
3. **视觉规范**：
   - 全屏暗色渐变背景。
   - 响应式文字排版（clamp）。
   - 液态玻璃（Glassmorphism）工具栏。
   - 丝滑的 0.6s 入场与 0.4s 出场动画。
4. **快捷键支持**：
   - `Space`：暂停/继续
   - `←` / `→`：上一句 / 下一句
   - `R`：切换随机/顺序模式

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
# 启动 Web 版本
npm run dev

# 启动 Electron 版本
npm run electron:dev
```

### 打包构建

```bash
# 构建 Web 版本
npm run build

# 构建 Electron 安装包
npm run electron:build
```

## 技术实现细节

- **动画系统**：基于 Framer Motion，采用 `cubic-bezier(0.22, 1, 0.36, 1)` 缓动曲线。
- **状态管理**：使用 `useReducer` 管理播放、暂停、索引和模式。
- **计时器**：通过 `requestAnimationFrame` + 时间戳差分实现精准计时，避免标签页休眠导致的计时漂移。
- **字体**：回退机制支持思源黑体 (Source Han Sans) / Inter。

## 性能表现

- 支持 1 万字长文本输入。
- 低 CPU 占用（<30%）。
- 响应式设计适配多种分辨率。
