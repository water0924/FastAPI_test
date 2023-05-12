import uvicorn

from typing import Union,List, Any

from enum import Enum

from fastapi import FastAPI, Query, Path, Body, Cookie, Header,status, HTTPException

from pydantic import BaseModel, EmailStr

app = FastAPI()

# 终端运行命令
# uvicorn main:app --reload
def more():
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("运行")

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ModelName(str, Enum):
    my = "my"
    name = "name"
    water = "water"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.name:
        return {"model_name": model_name, "message": "name"}
    if model_name.value == "water":
        return {"model_name": model_name, "message": "water"}
    return {"other"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id : int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "性别": item.is_offer}

@app.get("/query/")
def query_item(skip: int = 0, limit: int = 10):
    """
    默认查询参数为数字
    """
    return {"sum": skip + limit}

@app.get("/query/string")
def query_item(skip: str = "myname", limit: str = "江水根"):
    """
    默认查询参数为字符串
    """
    return {"sum": skip + limit}

@app.get("/query/more/{moreparam}")
def query_item(moreparam: str, w: bool , f: int, q: Union[str, None] = None):
    """
    含有多个查询参数
    """
    return {"moreparam": moreparam, "w": w, "q": q, "f": f}

# 数据模型继承BaseModel
class Base_test(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[str, None] = None

@app.post("/base_test/")
def creat_base_test(test: Base_test):
    """
    数据模型继承
    """
    return test

@app.post("/base_test/judge/")
def judge_base_test(test: Base_test):
    """
    判断请求体是否存在，如果存在通过if条件，输出一份新的数据
    """
    test_dict = test.dict()
    if test.tax:
        name_with_price = test.name + test.description
        test_dict.update({"name_with_price": name_with_price})
    return test_dict

# 额外的检验
@app.get("/set/max_length/")
def set_maxlength(q: Union[str, None] = Query(default=None, max_length=50)):
    """
    将Query用作查询参数的默认值，并将它的max_length参数设置为50
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/set/min_length/max_length")
def set_minlength_maxlength(q: Union[str, None] = Query(default=None, min_length=3, max_length=50)):
    """
    设置最小长度和最大长度
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/set/default/")
def set_default(q: Union[str, None] = Query(default="fixedquery", min_length=3, max_length=50)):
    """
    声明查询参数 q，使其 min_length 为 3，max_length为50，并且默认值为 fixedquery
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/required/parameter/")
def set_requierd_paramter(q: str = Query(default = ..., min_length = 3)):
    """
    使用省略号(...)声明必需参数
    """
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/define/group/value")
def define_group_value(q: Union[List[str], None] = Query(default=None)):
    """
    以一个Python list 的形式接收到查询参数q的多个值，如["foo","bar"]
    """
    result = {"q": q}
    return result

@app.get("/alias/param")
def alias_param(q: Union[List[str], None] = Query(default=None, alias="item-query")):
    """
    用alias参数声明一个别名，该别名用于在URL中查找查询参数值
    """
    results = {"items":[{"item_id": "foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q", q})
    return results

@app.get("/Path/{item_id}")
def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    """
    使用Path为路径参数声明相同类型的校验和元数据
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 请求体-多个参数
#dff
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/most/param/{item_id}")
def most_param(item_id: int,  item: Item, user: User, important: str):
    """
    该函数中有多个请求体参数
    """
    results = {"item_id": item_id ,"item":item, "user":user, "important": important}
    return results

@app.put("/body/{item_id}")
def body(item_id: int, item: Item = Body(embed=True)):
    """
    只有一个请求体参数，默认情况下请求体不含键传入，如果需要含有键，可使用一个特殊的Body参数embed
    以下没有body默认情况下为：
    {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
    }
    有body情况下为：
    {
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
    }   
    """
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/set/cookie/")
def set_cookie(ads_id: Union[str, None] = Cookie(default=None)):
    """
    定义 Cookie 参数
    你需要使用 Cookie 来声明 cookie 参数，否则参数将会被解释为查询参数
    """
    return {"ads_id": ads_id}

@app.get("/set/header/")
def set_header(user_agent: Union[str, None] = Header(default=None)):
    """
    默认情况下, Header 将把参数名称的字符从下划线 (_) 转换为连字符 (-) 来提取并记录 headers
    如果出于某些原因，你需要禁用下划线到连字符的自动转换，设置Header的参数 convert_underscores 为 False
    """
    return {"User-Agent": user_agent} 

@app.get("/deal/expection/")
def deal_expection(item_id: str):
    """
    客户端用 ID 请求的 param 不存在时，触发状态码为 404 的异常
    """
    param ={"foo": "The Foo Wreastlers"}
    if item_id not in param:
        raise HTTPException(status_code=404, detail = "Item not found")
    return {"item": param[item_id]}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)