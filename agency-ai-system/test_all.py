"""完整API测试脚本"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, url, data=None):
    """测试单个端点"""
    try:
        if method == "GET":
            r = requests.get(f"{BASE_URL}{url}", timeout=5)
        elif method == "POST":
            r = requests.post(f"{BASE_URL}{url}", json=data, timeout=5)
        elif method == "PUT":
            r = requests.put(f"{BASE_URL}{url}", json=data, timeout=5)
        elif method == "DELETE":
            r = requests.delete(f"{BASE_URL}{url}", timeout=5)
        else:
            return False, f"Unknown method: {method}"
        
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, f"Status: {r.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except Exception as e:
        return False, str(e)

def main():
    """运行所有测试"""
    print("=" * 60)
    print("AI多代理系统 - API功能测试")
    print("=" * 60)
    
    tests = [
        ("健康检查", "GET", "/health"),
        ("系统状态", "GET", "/api/system/status"),
        ("任务列表", "GET", "/api/tasks"),
        ("代理列表", "GET", "/api/agents"),
        ("大脑列表", "GET", "/api/brains"),
        ("模型列表", "GET", "/api/models"),
        ("心跳状态", "GET", "/api/heartbeat/status"),
        ("进度状态", "GET", "/api/progress/status"),
        ("日志查询", "GET", "/api/logs?limit=5"),
    ]
    
    results = []
    
    for name, method, url in tests:
        success, data = test_endpoint(name, method, url)
        results.append((name, success, data))
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name}")
        if success and isinstance(data, dict):
            # 打印部分数据
            if "cpu_usage" in data:
                print(f"       CPU: {data['cpu_usage']}%, Memory: {data['memory_usage']}%")
            elif "total_tasks" in data:
                print(f"       Tasks: {data.get('total_tasks', 0)}")
        elif success and isinstance(data, list):
            print(f"       Count: {len(data)}")
    
    # 测试创建任务
    print("\n--- 测试创建任务 ---")
    success, data = test_endpoint("创建任务", "POST", "/api/tasks", {
        "title": "测试任务",
        "description": "这是一个测试任务",
        "priority": 5
    })
    results.append(("创建任务", success, data))
    status = "PASS" if success else "FAIL"
    print(f"[{status}] 创建任务")
    if success:
        print(f"       Task ID: {data.get('id', 'N/A')}")
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, _ in results:
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
