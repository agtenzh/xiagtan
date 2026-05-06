"""测试配置"""
import pytest
from app.core.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """设置测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
