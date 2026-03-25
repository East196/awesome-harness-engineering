# 前端设计 Harness 示例

> 实现 Anthropic 论文中的前端设计评估循环

## 核心特性

- ✅ 生成器-评估器循环架构
- ✅ 四维评估标准（设计质量、原创性、工艺、功能性）
- ✅ Playwright 自动化测试
- ✅ 多轮迭代优化

## 评估标准

```python
CRITERIA = {
    "design_quality": {
        "weight": 0.35,
        "description": "设计是否像一个统一的整体",
        "aspects": ["色彩和谐", "排版层级", "视觉一致性"]
    },
    "originality": {
        "weight": 0.30,
        "description": "是否有定制的创意决策",
        "aspects": ["避免模板", "独特风格", "创新交互"]
    },
    "craft": {
        "weight": 0.20,
        "description": "技术执行质量",
        "aspects": ["代码规范", "响应式", "性能"]
    },
    "functionality": {
        "weight": 0.15,
        "description": "可用性独立于美学",
        "aspects": ["导航清晰", "交互反馈", "无障碍"]
    }
}
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt
playwright install

# 运行示例
python examples/design_website.py "创建一个荷兰艺术博物馆网站"
```

## 工作流程

```
用户输入 → Planner → 设计规格
                ↓
          Generator (HTML/CSS/JS)
                ↓
          Evaluator (Playwright 测试)
                ↓
          评分 + 反馈
                ↓
          迭代优化 (5-15 轮)
                ↓
          最终输出
```

## 输出示例

```
🎨 Frontend Design Harness

需求: 创建一个荷兰艺术博物馆网站

[Sprint 1/10]
🎨 生成设计...
✅ 代码生成完成

🔍 评估中...
┌─────────────────┬────────┬────────────────┐
│ 标准            │ 分数   │ 反馈           │
├─────────────────┼────────┼────────────────┤
│ 设计质量        │ 0.65   │ 色彩和谐但缺乏 │
│ 原创性          │ 0.55   │ 过于模板化     │
│ 工艺            │ 0.80   │ 代码质量良好   │
│ 功能性          │ 0.75   │ 导航清晰       │
├─────────────────┼────────┼────────────────┤
│ 总分            │ 0.69   │ 需要改进       │
└─────────────────┴────────┴────────────────┘

[Sprint 2/10]
🎨 重新设计...
💡 创意方向: 空间体验

...

[Sprint 10/10]
🎉 达到质量标准!
✨ 创意飞跃: 3D 画廊体验
📁 输出: ./output/art-museum/index.html
```

## 创意飞跃案例

在第 10 轮迭代中，系统从传统的深色落地页转变为**空间体验**：

- CSS 3D 透视渲染的棋盘地板
- 自由悬挂的艺术品
- 门洞导航替代滚动

这种创意飞跃在单次生成中从未出现。

## 配置

```yaml
# config.yaml
frontend:
  iterations: 10
  min_score: 0.85
  
  playwright:
    viewport: { width: 1920, height: 1080 }
    screenshots: true
    
  style_prompts:
    - "博物馆品质"
    - "现代简约"
    - "艺术感"
```
