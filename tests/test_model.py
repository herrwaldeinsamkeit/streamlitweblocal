import joblib
import os

def test_model_exists():
    # 检查模型文件是否存在
    assert os.path.exists("complex_model_pipeline.pkl")

def test_model_loading():
    # 检查模型是否能被成功加载
    model = joblib.load("complex_model_pipeline.pkl")
    assert model is not None
