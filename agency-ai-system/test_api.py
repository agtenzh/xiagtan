"""API测试脚本"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("=" * 50)
    print("1. 测试健康检查")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {r.status_code}")
        print(f"响应: {r.json()}")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_system_status():
    """测试系统状态"""
    print("\n" + "=" * 50)
    print("2. 测试系统状态")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/system/status")
        print(f"状态码: {r.status_code}")
        print(f"响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_create_task():
    """测试创建任务"""
    print("\n" + "=" * 50)
    print("3. 测试创建任务")
    print("=" * 50)
    try:
        data = {
            "title": "测试任务",
            "description": "这是一个测试任务",
            "priority": 5
        }
        r = requests.post(f"{BASE_URL}/api/tasks", json=data)
        print(f"状态码: {r.status_code}")
        print(f"响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return r.status_code == 200, r.json().get("id")
    except Exception as e:
        print(f"错误: {e}")
        return False, None

def test_list_tasks():
    """测试任务列表"""
    print("\n" + "=" * 50)
    print("4. 测试任务列表")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/tasks")
        print(f"状态码: {r.status_code}")
        print(f"任务数量: {len(r.json())}")
        for task in r.json():
            print(f"  - {task['title']} ({task['status']})")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_create_agent():
    """测试创建代理"""
    print("\n" + "=" * 50)
    print("5. 测试创建代理")
    print("=" * 50)
    try:
        data = {
            "name": "测试代理",
            "description": "这是一个测试代理",
            "category": "development",
            "model_provider": "openai",
            "model_name": "gpt-4"
        }
        r = requests.post(f"{BASE_URL}/api/agents", json=data)
        print(f"状态码: {r.status_code}")
        print(f"响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return r.status_code == 200, r.json().get("id")
    except Exception as e:
        print(f"错误: {e}")
        return False, None

def test_list_agents():
    """测试代理列表"""
    print("\n" + "=" * 50)
    print("6. 测试代理列表")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/agents")
        print(f"状态码: {r.status_code}")
        print(f"代理数量: {len(r.json())}")
        for agent in r.json():
            print(f"  - {agent['name']} ({agent['category']})")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_list_brains():
    """测试大脑列表"""
    print("\n" + "=" * 50)
    print("7. 测试大脑列表")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/brains")
        print(f"状态码: {r.status_code}")
        print(f"大脑数量: {len(r.json())}")
        for brain in r.json():
            print(f"  - {brain['name']} ({brain['brain_type']})")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_heartbeat():
    """测试心跳状态"""
    print("\n" + "=" * 50)
    print("8. 测试心跳状态")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/heartbeat/status")
        print(f"状态码: {r.status_code}")
        print(f"响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_progress():
    """测试进度监控"""
    print("\n" + "=" * 50)
    print("9. 测试进度监控")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/progress/status")
        print(f"状态码: {r.status_code}")
        print(f"响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_logs():
    """测试日志查询"""
    print("\n" + "=" * 50)
    print("10. 测试日志查询")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/api/logs?limit=5")
        print(f"状态码: {r.status_code}")
        print(f"日志数量: {len(r.json())}")
        for log in r.json():
            print(f"  - [{log['level']}] {log['message']}")
        return r.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("AI多代理系统 - API功能测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("健康检查", test_health()))
    results.append(("系统状态", test_system_status()))
    
    task_result, task_id = test_create_task()
    results.append(("创建任务", task_result))
    
    results.append(("任务列表", test_list_tasks()))
    
    agent_result, agent_id = test_create_agent()
    results.append(("创建代理", agent_result))
    
    results.append(("代理列表", test_list_agents()))
    results.append(("大脑列表", test_list_brains()))
    results.append(("心跳状态", test_heartbeat()))
    results.append(("进度监控", test_progress()))
    results.append(("日志查询", test_logs()))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n所有测试通过！")
        return 0
    else:
        print(f"\n有 {total - passed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
