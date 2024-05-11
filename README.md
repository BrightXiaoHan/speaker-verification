# 项目名称
声纹识别项目

## 声纹比对
请求方式：GET

请求路径 `http://ip:port/yuyispeech/vector/score`

请求参数：
| 参数名 | 参数类型 | 是否必填 | 备注 |
|  ---  |---  | --- |   ---   |
|   enroll\_audio\_url  |  str  |   是   |  声纹音频url路径   |
|   test\_audio\_url  |  String  |   是   |    待验证音频url路径    |
|   sample\_rate  |  int  |   否   |    音频采样率，默认是16000，可以指定8000    |

curl请求示例
```shell
curl --location --request POST 'http://127.0.0.1:10090/yuyispeech/vector/score?enroll_audio_url=http://39.105.167.2:9529/uploads/asrdir/2024/02/01/16616686965_b93da13a-12c0-489c-9e16-a389f76b6e85_0.wav&test_audio_url=http://39.105.167.2:9529/uploads/asrdir/2024/04/22/16616686965_34dee04f-65e6-4069-a830-bd84d721a744_0.wav&sample_rate=8000'
```

返回参数
```json
{
    "success": true,
    "code": 200,
    "message": {
        "description": "success"
    },
    "result": {
        "score": 0.7143293411779446
    }
}
```


## 声纹库查询

### 接口通用返回值

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

### 声纹库添加接口
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

### 声纹库删除接口
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

### 声纹推理接口

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
