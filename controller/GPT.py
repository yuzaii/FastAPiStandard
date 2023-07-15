from fastapi import APIRouter

TestRouter = APIRouter(prefix='/test', tags=['测试相关api'])


@TestRouter.get("/test", summary='测试')
def test():
    return {'code': 20000, 'msg': '测试成功'}
