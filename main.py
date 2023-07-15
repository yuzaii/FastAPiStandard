from fastapi import FastAPI
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from controller.GPT import TestRouter

# docs_url=None, redoc_url=None 禁用自带的docs文档接口
app = FastAPI(docs_url=None, redoc_url=None)
# 因为下面要用到接口静态文件，所以，这里挂载一下
app.mount('/static', StaticFiles(directory='./static'))

app.add_middleware(
    CORSMiddleware,
    # 允许跨域
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 利用fastapi提供的函数，生成文档网页 下面两个都是
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
        # 文档页面一开始折叠
        swagger_ui_parameters={"docExpansion": None},
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js")


# 将首页重定向 include_in_schema不包含到文档中
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


app.include_router(TestRouter)
if __name__ == '__main__':
    uvicorn.run(app='main:app',
                # 主机地址
                host="127.0.0.1",
                # 端口号
                port=8000,
                reload=True)
