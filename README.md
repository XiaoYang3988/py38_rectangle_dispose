# py38_rectangle_dispose
在像素坐标内，根据矩形数据与需要绘制矩形的长度宽度与连接线的角度与长度，绘制与该矩形相连接的矩形与连接线，绘制的矩形与连接线段不能和其他所有矩形与线段相交

#### data.txt
```
0 4347 3893 4347 3935 4452 3935 4452 3893
```
开头第一个数字为无效数据，第一个数字之后的数字，每两个组成一个(u,v)像素坐标，每行数据结束符为\r\n

#### main

```javascript
def main():
    time_start = time.time()

    # 读取文本内全部文本数据
    t = fdp.read_all_text('data.txt', 'UTF-8')
    # 根据字符串数据转化成class rectangle
    rectangle = pg.string_turn_rectangle_list(t, " ")
    # 过滤面积等于0的数据
    rectangle = list(x for x in rectangle if math.isclose(0.0, x.area, abs_tol = 1e-6) == False)
    
    # rectangle_describe_list 的数据格式
    rectangle_describe_list = list({'rectangle':x, 'describe_list':list(), } for x in rectangle)
    # 描述框长度
    describe_length = 300
    # 描述框宽度
    describe_breadth = 300
    # 线段长度
    line_length = 500
    # 角度
    angle = 45.0
    # 矩形和描述框的间隔
    rectangle_and_describe_interval = 5.0
    # 描述框和描述框的间隔
    describe_and_describe_interval = 8.0
    
    # 循环[{'rectangle':x, 'describe_list':list()] 判断rectangle: value是不是可以生成连接线段和描述框
    result = pg.loop_judging_line_and_all_line_return_describe_rectangle(rectangle_describe_list = rectangle_describe_list, describe_length = describe_length,
                                                                                            describe_breadth = describe_breadth, line_length = line_length,
                                                                                            angle = angle, rectangle_and_describe_interval = rectangle_and_describe_interval,
                                                                                            describe_and_describe_interval = describe_and_describe_interval)
    
    
    modify_rectangle = list(x['rectangle'] for x in result)
    modify_describe = list(y for x in result if len(x['describe_list']) != 0 for y in x['describe_list'])
    time_end = time.time()
    print('总共的时间为:', round(time_end - time_start, 0),'s')
    pg.matplotlib_draw(modify_rectangle, modify_describe)

    # tuple turn dict
    dict_result = list({'rectangle': pg.rectangle_data_turn_dict(x['rectangle']), 'describe_list':list(pg.rectangle_data_turn_dict(y) for y in x['describe_list'])} for x in result)
    fdp.save_data_text('result_data.txt', 'UTF-8', json.dumps(dict_result))
```

#### result_data.txt
可命名元组转json数据，result_data.txt是输出文本文件
