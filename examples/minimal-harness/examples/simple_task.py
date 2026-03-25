#!/usr/bin/env python3
"""
最小 Harness 示例 - 简单任务
演示如何使用 MinimalHarness 完成一个简单任务
"""

import asyncio
import sys
sys.path.insert(0, '..')

from core.harness import MinimalHarness


async def main():
    """运行简单任务示例"""
    
    print("=" * 60)
    print("🚀 Minimal Harness 示例")
    print("=" * 60)
    
    # 创建 Harness 实例
    harness = MinimalHarness(
        max_iterations=5,
        min_quality_score=0.8,
        debug=True
    )
    
    # 定义任务
    task = "创建一个简单的待办事项应用，支持添加、完成和删除任务"
    
    print(f"\n📋 任务: {task}\n")
    
    # 运行 Harness
    try:
        result = await harness.run(task)
        
        # 显示结果
        print("\n" + "=" * 60)
        print("✅ 执行完成!")
        print("=" * 60)
        print(f"\n📊 结果统计:")
        print(f"   • 产品名称: {result['spec']['title']}")
        print(f"   • 质量分数: {result['quality_score']:.2f}/1.0")
        print(f"   • 迭代次数: {result['iterations']}")
        print(f"   • 代码长度: {len(result['code'])} 字符")
        
        print(f"\n📦 功能列表:")
        for i, feature in enumerate(result['spec']['features'], 1):
            print(f"   {i}. {feature}")
        
        print(f"\n🔧 技术栈:")
        for layer, tech in result['spec']['tech_stack'].items():
            print(f"   • {layer}: {tech}")
        
        print(f"\n📈 迭代历史:")
        for record in result['history']:
            print(f"   Sprint {record['sprint']}: "
                  f"分数={record['quality_score']:.2f}, "
                  f"代码={record['code_length']}字符")
        
        print(f"\n💡 提示:")
        print("   这是一个演示实现，实际使用需要:")
        print("   1. 配置真实的 LLM API (Claude/OpenAI)")
        print("   2. 实现真正的代码生成逻辑")
        print("   3. 添加更完善的评估标准")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        raise


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
