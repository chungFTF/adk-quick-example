"""
Agent Validation Script
測試和驗證 multi-agent 系統的各項功能
"""

import asyncio
import sys
from pathlib import Path

# 添加項目路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import uuid

# 導入 root_agent
# 注意：目錄名稱是 example-agent（有連字號），需要直接添加到路徑
import importlib.util
spec = importlib.util.spec_from_file_location(
    "agent_module",
    project_root / "example-agent" / "agent.py"
)
agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_module)
root_agent = agent_module.root_agent

APP_NAME = "validation_test"
USER_ID = "test_user"


async def test_agent(prompt: str, test_name: str = ""):
    """測試 agent 並返回回應"""
    session_service = InMemorySessionService()
    session_id = f"{APP_NAME}-{uuid.uuid4().hex[:8]}"
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )
    
    final_response_text = "無法取得回應"
    tool_calls = []
    
    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if (
                event.content
                and event.content.parts
                and event.content.parts[0].function_call
            ):
                func_call = event.content.parts[0].function_call
                tool_call = {
                    "tool_name": func_call.name,
                    "tool_input": dict(func_call.args),
                }
                tool_calls.append(tool_call)
            
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text
                break
    
    except Exception as e:
        print(f"❌ 測試 '{test_name}' 發生錯誤: {e}")
        return None
    
    return {
        "test_name": test_name,
        "prompt": prompt,
        "response": final_response_text,
        "tool_calls": tool_calls
    }


async def run_validation_tests():
    """執行所有驗證測試"""
    
    print("=" * 80)
    print("Agent 驗證測試")
    print("=" * 80)
    print()
    
    # 定義測試案例
    test_cases = [
        # Math Agent 測試
        {
            "name": "數學計算 - 基本算術",
            "prompt": "What is 25% of 480?",
            "expected_agent": "math_agent"
        },
        {
            "name": "數學計算 - 平均數",
            "prompt": "Calculate the average of 10, 20, 30, 40, 50",
            "expected_agent": "math_agent"
        },
        {
            "name": "數學計算 - 百分比",
            "prompt": "如果一件商品原價 1000 元，打 8 折後是多少錢？",
            "expected_agent": "math_agent"
        },
        
        # Translation Agent 測試
        {
            "name": "翻譯 - 英文到西班牙文",
            "prompt": "Translate 'Hello, how are you?' to Spanish",
            "expected_agent": "translation_agent"
        },
        {
            "name": "翻譯 - 中文到英文",
            "prompt": "請將 '你好，很高興認識你' 翻譯成英文",
            "expected_agent": "translation_agent"
        },
        {
            "name": "翻譯 - 單字解釋",
            "prompt": "What does 'serendipity' mean?",
            "expected_agent": "translation_agent"
        },
        
        # Root Agent 路由測試
        {
            "name": "路由測試 - 混合查詢",
            "prompt": "Calculate the average of 10, 20, 30, 40, 50 and translate the result to French",
            "expected_agent": "both"
        },
        {
            "name": "路由測試 - 不相關查詢",
            "prompt": "What is the capital of France?",
            "expected_agent": "root_agent"
        },
    ]
    
    results = []
    
    # 執行所有測試
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] 測試: {test_case['name']}")
        print(f"  查詢: {test_case['prompt']}")
        
        result = await test_agent(test_case['prompt'], test_case['name'])
        
        if result:
            results.append({
                **result,
                "expected_agent": test_case['expected_agent']
            })
            
            print(f"  ✅ 回應已收到")
            if result['tool_calls']:
                print(f"  工具調用: {len(result['tool_calls'])} 次")
        else:
            results.append({
                "test_name": test_case['name'],
                "prompt": test_case['prompt'],
                "response": None,
                "expected_agent": test_case['expected_agent']
            })
            print(f"  ❌ 測試失敗")
        
        print()
    
    # 顯示詳細結果
    print("=" * 80)
    print("測試結果摘要")
    print("=" * 80)
    print()
    
    for result in results:
        print(f"測試: {result['test_name']}")
        print(f"查詢: {result['prompt']}")
        if result.get('response'):
            # 顯示回應的前 200 個字元
            response_preview = result['response'][:200]
            if len(result['response']) > 200:
                response_preview += "..."
            print(f"回應: {response_preview}")
        else:
            print("回應: ❌ 無回應")
        
        if result.get('tool_calls'):
            print(f"工具調用:")
            for tool_call in result['tool_calls']:
                print(f"  - {tool_call['tool_name']}")
        
        print("-" * 80)
        print()
    
    # 統計
    success_count = sum(1 for r in results if r.get('response'))
    total_count = len(results)
    
    print("=" * 80)
    print(f"測試完成: {success_count}/{total_count} 通過")
    print("=" * 80)
    
    return results


async def interactive_test():
    """互動式測試模式"""
    print("=" * 80)
    print("互動式 Agent 測試")
    print("=" * 80)
    print("輸入 'quit' 或 'exit' 結束")
    print()
    
    session_service = InMemorySessionService()
    session_id = f"{APP_NAME}-{uuid.uuid4().hex[:8]}"
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )
    
    while True:
        try:
            prompt = input("\n請輸入查詢: ").strip()
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("結束測試")
                break
            
            if not prompt:
                continue
            
            print("\n處理中...")
            
            final_response_text = "無法取得回應"
            tool_calls = []
            
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session_id,
                new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
            ):
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].function_call
                ):
                    func_call = event.content.parts[0].function_call
                    tool_call = {
                        "tool_name": func_call.name,
                        "tool_input": dict(func_call.args),
                    }
                    tool_calls.append(tool_call)
                
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response_text = event.content.parts[0].text
                    break
            
            print(f"\n回應: {final_response_text}")
            
            if tool_calls:
                print(f"\n工具調用:")
                for tool_call in tool_calls:
                    print(f"  - {tool_call['tool_name']}")
        
        except KeyboardInterrupt:
            print("\n\n結束測試")
            break
        except Exception as e:
            print(f"\n❌ 錯誤: {e}")


def main():
    """主函數"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_test())
    else:
        asyncio.run(run_validation_tests())


if __name__ == "__main__":
    main()
