from fastapi import FastAPI

# 初始化 FastAPI 应用
app = FastAPI(title="Expandable Backend API")

# 根接口测试用
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 上传接口占位
@app.post("/upload")
def upload_file():
    return {"message": "Upload endpoint placeholder"}
