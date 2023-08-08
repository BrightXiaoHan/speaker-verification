# 项目名称
声纹识别项目

# 接口

## 接口通用返回值

| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   code  |  int  |   是   |   返回编码，200表示成功，500表示失败   |
|   msg  |  String  |   是   |    返回的消息体    |
|   data  |  obj  |   否   |    具体的业务数据    |

返回值示例：
```json
{
    "code": 200,
    "msg": ""
}
```

## 声纹库添加接口
添加、更新训练数据示例（`/voiceprint/update`）

入参：
| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   id  |  int  |   是   |   用户ID   |
|   name  |  String  |   是   |    用户名称    |
|   sampling_rate  |  String  |   是   |    采样率，8000或者16000    |
|   data  |  String  |   是   |    base64编码声纹数据    |

示例：
```json
{
    "id": "1",
    "name": "张三",
    "sampling_rate": "16000",
    "data":"",
}
```

返回值见通用返回值

## 声纹库删除接口
删除声纹接口数据示例（`/voiceprint/delete`）

入参：
| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   id  |  int  |   是   |   用户ID   |

示例：
```json
{
    "id": "1"
}
```

返回值见通用返回值

## 声纹推理接口

删除声纹接口数据示例（`/voiceprint/reasoning`）

入参：
| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   sampling_rate  |  String  |   是   |    采样率，8000或者16000    |
|   data  |  String  |   是   |   base64编码录音数据   |

示例：
```json
{
    "sampling_rate": "16000",
    "data": "base64加密数据"
}
```

返回值:

| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   code  |  int  |   是   |   返回编码，200表示成功，500表示失败   |
|   msg  |  String  |   是   |    返回的消息体    |
|   data  |  obj  |   否   |    具体的业务数据    |
|   data.id  |  int  |   是   |    匹配用户ID    |
|   data.name  |  String  |   是   |    匹配用户名称    |
|   data.score  |  String  |   是   |    匹配分值    |
```json
{
    "code": 200,
    "msg": "",
    "data":[
        {
            "id":"1",
            "name":"张三",
            "score":"0.97"
        }
    ]
}
```
