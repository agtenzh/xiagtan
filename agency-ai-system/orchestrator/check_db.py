"""检查数据库状态"""
import sys
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.models import Agent, Brain, ModelProvider

db = SessionLocal()

# 检查代理
agents = db.query(Agent).all()
print(f"=== 数据库中的代理: {len(agents)}个 ===")
for a in agents:
    print(f"  [{a.category}] {a.name}")
    print(f"    模型: {a.model_provider}/{a.model_name}")
    print(f"    提示词: {'有' if a.prompt_template else '空'} ({len(a.prompt_template) if a.prompt_template else 0}字符)")
    print()

# 检查大脑
brains = db.query(Brain).all()
print(f"=== 数据库中的大脑: {len(brains)}个 ===")
for b in brains:
    print(f"  [{b.brain_type}] {b.name} - 代理: {b.agents}")

# 检查模型
models = db.query(ModelProvider).all()
print(f"\n=== 数据库中的模型: {len(models)}个 ===")
for m in models:
    print(f"  {m.name} - {m.base_url}")

db.close()
