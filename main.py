from typing import Union

from enum import Enum

from fastapi import FastAPI, Query

from pydantic import BaseModel

app = FastAPI()

# 终端运行命令
# uvicorn main:app --reload

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
# test  dd  dd  ddf  gfggs 
