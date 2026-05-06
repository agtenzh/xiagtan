"""检查API返回的数据"""
import requests
import json

# 检查代理
print("=== API代理数据 ===")
try:
    r = requests.get("http://localhost:8000/api/agents", timeout=5)
    print(f"状态码: {r.status_code}")
    agents = r.json()
    print(f"代理数量: {len(agents)}")
    for a in agents[:3]:
        print(f"  [{a['category']}] {a['name']}")
        print(f"    模型: {a['model_provider']}/{a['model_name']}")
        pt = a.get('prompt_template') or ''
        print(f"    提示词: {'有' if pt else '空'} ({len(pt)}字符)")
except Exception as e:
    print(f"错误: {e}")

# 检查大脑
print("\n=== API大脑数据 ===")
try:
    r = requests.get("http://localhost:8000/api/brains", timeout=5)
    print(f"状态码: {r.status_code}")
    print(f"响应: {r.text[:500]}")
    if r.status_code == 200 and r.text:
        brains = r.json()
        print(f"大脑数量: {len(brains)}")
        for b in brains:
            print(f"  [{b['brain_type']}] {b['name']} - 代理: {b.get('agents', [])}")
except Exception as e:
    print(f"错误: {e}")

# 检查模型
print("\n=== API模型数据 ===")
try:
    r = requests.get("http://localhost:8000/api/models", timeout=5)
    print(f"状态码: {r.status_code}")
    if r.status_code == 200 and r.text:
        models = r.json()
        print(f"模型数量: {len(models)}")
        for m in models:
            print(f"  {m['name']} - {m['base_url']}")
except Exception as e:
    print(f"错误: {e}")
