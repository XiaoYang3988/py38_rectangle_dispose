import math
import numpy
import itertools
import traceback
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D    

from collections import namedtuple
from functools import lru_cache

__rectangle_tuple = None
__coordinates = None
__describe_tuple = None
__line_tuple = None

def __init():
    global __rectangle
    global __coordinates 
    global __describe_rectangle
    global __line
    global __assemble 
    
    __rectangle = namedtuple('rectangle', ['line_invalid_data', 'coordinates_list', 'length', 'breadth', 'area'])
    __coordinates = namedtuple('coordinates', ['x', 'y'])    
    __describe_rectangle = namedtuple('describe_rectangle', ['line_invalid_data', 'coordinates_list', 'length', 'breadth', 'area', 'line'])
    __line = namedtuple('line', ['min_coordinates', 'max_coordinates', 'line_slope'])
    __assemble = namedtuple('assemble', ['min', 'max'])

# 线段函数
@lru_cache(maxsize = 2**16)
def __line_func(n: tuple = None, x: float = None):
    if math.isclose(90.0, n.line_slope, rel_tol = 1e-6):
        if math.isclose(n.min_coordinates.x, x, rel_tol = 1e-6):
            return __assemble(n.min_coordinates.y, n.max_coordinates.y)
        else:
            return None
    elif math.isclose(270.0, n.line_slope, rel_tol = 1e-6):
        if math.isclose(n.min_coordinates.x, x, rel_tol = 1e-6):
            return __assemble(n.max_coordinates.y, n.min_coordinates.y)  
        else:
            return None
    else:    
        return math.tan(math.radians(n.line_slope))*(x - n.min_coordinates.x) + n.min_coordinates.y
    
# 根据坐标，斜率，长度 生成新线段(class line)
def __line_generate(t: tuple = None, s: float = None, l: float = None):
    '''
    坐标，斜率，长度
    '''
    if math.isclose(0.0, s, abs_tol = 1e-6) or math.isclose(360.0, s, rel_tol = 1e-6):
        return __line(__coordinates(t.x, t.y), __coordinates(t.x + l, t.y), s)

    if math.isclose(180.0, s, rel_tol = 1e-6):
        return __line(__coordinates(t.x, t.y), __coordinates(t.x - l, t.y), s)

    if math.isclose(90.0, s, rel_tol = 1e-6):
        return __line(__coordinates(t.x, t.y), __coordinates(t.x, t.y + l), s)
    
    if math.isclose(270.0, s, rel_tol = 1e-6):
        return __line(__coordinates(t.x, t.y), __coordinates(t.x, t.y - l), s)
    
    if s > 90.0 and s < 270.0:
        return __line(__coordinates(t.x + l * math.cos(math.radians(s)), t.y + l * math.sin(math.radians(s))), __coordinates(t.x, t.y), s)
    else:    
        return __line(__coordinates(t.x, t.y), __coordinates(t.x + l * math.cos(math.radians(s)), t.y + l * math.sin(math.radians(s))), s)
# 计算斜率返回线段角度
def __calculate_slope_angle(f: tuple = None, f1: tuple = None):
    if math.isclose(0.0, abs(f1.y - f.y), abs_tol = 1e-6):
        return 0.0
    if math.isclose(0.0, abs(f1.x - f.x), abs_tol = 1e-6):
        return 90.0
    return math.degrees( math.atan((f1.y - f.y) / (f1.x - f.x)) )
# 返回线段上的点的集合，点的原子间隔为n
def __reutrn_line_coordinates_collection(t: tuple = None, n: float = 1.0):
    '''
    获得全部线段点的集合
    '''
    subset_x = __assemble(t.min_coordinates.x, t.max_coordinates.x) 
    subset_y = __assemble(t.min_coordinates.y, t.max_coordinates.y) 
    if math.isclose(90.0, t.line_slope, rel_tol = 1e-6) or math.isclose(270.0, t.line_slope, rel_tol = 1e-6):
        return list(__coordinates( t.max_coordinates.x, x ) for x in numpy.arange(subset_y.min, int(subset_y.max) + 1.0, n))
    
    return list(__coordinates( float(x), __line_func(t, x) ) for x in numpy.arange(subset_x.min, int(subset_x.max) + 1.0, n))

# 列表内对象比较或检验函数
def __list_comparison_func(l: tuple = None, f: object = None):
    '''
    函数作用：
        列表内对象比较或检验函数
    参数：
        l: 列表
        f: 对象或者函数
    return: 
        true or false
    '''
    for x in range(0, len(l), 1):
        for y in range(x + 1, len(l), 1):
            if f(l[x]) != f(l[y]):
                return False    
    return True

# 获取交集
@lru_cache(maxsize = 2**16)
def __intersections_of_two_tuples(t: tuple = None, t1: tuple = None):
    
    new_t = lambda t:__assemble(t.max, t.min) if t.min > t.max else __assemble(t.min, t.max)

    gather = new_t(t)
    gather_1 = new_t(t1)
    
    if gather.max < gather_1.max:
        min_x = gather
        max_x = gather_1        
    else:
        min_x = gather_1
        max_x = gather

    if max_x.min > min_x.max:
        return None
    
    l = list()
    l.append(min_x.min)
    l.append(min_x.max)
    l.append(max_x.max)
    l.append(max_x.min)
    l.sort(reverse = False)
    
    return __assemble(l[1], l[2])

# 修改矩形定义域最小值的范围
def modify_rectangle_min_domain_of_definition(l: tuple = None, n: float = None):
    '''
    函数作用：
        修改矩形定义域最小值的范围
    参数：
        l: class rectangle
        n: 修改范围 float
    return: 
        class rectangle or None    
    '''
    try:
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x) + n
        max_x = float(l.coordinates_list[0].x + l.length)
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y)
        max_y = float(l.coordinates_list[0].y + l.breadth)
        
        if max_x - min_x <= 0.0:
            return None
        if min_x < 0:
            return None
        
        rectangle = __rectangle(l.line_invalid_data, [__coordinates(min_x, min_y), __coordinates(max_x, min_y), __coordinates(min_x, max_y), __coordinates(max_x, max_y)], max_x - min_x, max_y - min_y, (max_x - min_x) * (max_y - min_y) )
        return rectangle
    except Exception as e:
        traceback.print_exc()  
        return None   
# 修改矩形定义域最大值的范围
def modify_rectangle_max_domain_of_definition(l: tuple = None, n: float = None):
    '''
    函数作用：
        修改矩形定义域最大值的范围
    参数：
        l: class rectangle
        n: 修改范围 float
    return: 
        class rectangle or None    
    '''
    try:
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x)
        max_x = float(l.coordinates_list[0].x + l.length) + n
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y)
        max_y = float(l.coordinates_list[0].y + l.breadth)
        
        if max_x - min_x <= 0.0:
            return None
        if max_x < 0:
            return None
        rectangle = __rectangle(l.line_invalid_data, [__coordinates(min_x, min_y), __coordinates(max_x, min_y), __coordinates(min_x, max_y), __coordinates(max_x, max_y)], max_x - min_x, max_y - min_y, (max_x - min_x) * (max_y - min_y) )
        return rectangle
    except Exception as e:
        traceback.print_exc()  
        return None   
# 修改矩形值域最小值的范围
def modify_rectangle_min_value_domain(l: tuple = None, n: float = None):
    '''
    函数作用：
        修改矩形值域最小值的范围
    参数：
        l: class rectangle
        n: 修改范围 float
    return: 
        class rectangle or None    
    '''
    try:
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x)
        max_x = float(l.coordinates_list[0].x + l.length)
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y) + n
        max_y = float(l.coordinates_list[0].y + l.breadth)
        
        if max_y - min_y <= 0.0:
            return None
        if min_y < 0:
            return None
        rectangle = __rectangle(l.line_invalid_data, [__coordinates(min_x, min_y), __coordinates(max_x, min_y), __coordinates(min_x, max_y), __coordinates(max_x, max_y)], max_x - min_x, max_y - min_y, (max_x - min_x) * (max_y - min_y) )
        return rectangle
    except Exception as e:
        traceback.print_exc()  
        return None   
# 修改矩形值域最大值的范围
def modify_rectangle_max_value_domain(l: tuple = None, n: float = None):
    '''
    函数作用：
        修改矩形值域最大值的范围
    参数：
        l: class rectangle
        n: 修改范围 float
    return: 
        class rectangle or None    
    '''
    try:
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x)
        max_x = float(l.coordinates_list[0].x + l.length)
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y)
        max_y = float(l.coordinates_list[0].y + l.breadth) + n
        
        if max_y - min_y <= 0.0:
            return None
        if max_y < 0:
            return None
        rectangle = __rectangle(l.line_invalid_data, [__coordinates(min_x, min_y), __coordinates(max_x, min_y), __coordinates(min_x, max_y), __coordinates(max_x, max_y)], max_x - min_x, max_y - min_y, (max_x - min_x) * (max_y - min_y) )
        return rectangle
    except Exception as e:
        traceback.print_exc()  
        return None           
# 修改定义域值域最大最小值
def modify_rectangle_value_domain_and_domain_of_definition(l: tuple = None, n: float = None):
    '''
    函数作用：
        修改定义域值域最大最小值
    参数：
        l: class rectangle
        n: 修改范围 float
    return: 
        class rectangle or None    
    '''
    try:
        judge_none = lambda n: True if n == None else False
        
        if type(l) == __rectangle:
            rectangle = __rectangle(l.line_invalid_data, l.coordinates_list, l.length, l.breadth, l.area)
            rectangle = modify_rectangle_min_domain_of_definition(rectangle, -n)
            if judge_none(rectangle):
                return None
            rectangle = modify_rectangle_max_domain_of_definition(rectangle, n)
            if judge_none(rectangle):
                return None            
            rectangle = modify_rectangle_min_value_domain(rectangle, -n)
            if judge_none(rectangle):
                return None
            rectangle = modify_rectangle_max_value_domain(rectangle, n)
            if judge_none(rectangle):
                return None
            return rectangle
        elif type(l) == __describe_rectangle:
            describe_rectangle = __describe_rectangle(l.line_invalid_data, l.coordinates_list, l.length, l.breadth, l.area, l.line)
            describe_rectangle = modify_rectangle_min_domain_of_definition(describe_rectangle, -n)
            if judge_none(describe_rectangle):
                return None
            describe_rectangle = modify_rectangle_max_domain_of_definition(describe_rectangle, n)
            if judge_none(describe_rectangle):
                return None
            describe_rectangle = modify_rectangle_min_value_domain(describe_rectangle, -n)
            if judge_none(describe_rectangle):
                return None
            describe_rectangle = modify_rectangle_max_value_domain(describe_rectangle, n)
            if judge_none(describe_rectangle):
                return None
            return __describe_rectangle(describe_rectangle.line_invalid_data, describe_rectangle.coordinates_list, describe_rectangle.length, describe_rectangle.breadth, describe_rectangle.area, l.line)
                    
    except Exception as e:
        traceback.print_exc()  
        return None    

# string转rectangle数据
def string_turn_rectangle_list(s: str = None, s_1: str = None):
    '''
    函数作用：
        读取字符串，根据字符串每行分隔符解析数据，最后返回list(class rectangle)数据
    参数：
        s: 字符串(string)
        s_1: 分隔字符(string)
    return: 
        list(class rectangle) or None
    '''
    try:
        if s_1 != ',':
            s1 = s.replace(s_1, ',')
        else:
            s1 = s  

        # 原始字符串数据列表
        s_list = s1.splitlines(False)
        # 无效数据
        s_list_invalid = list(i[:i.find(',')] for i in s_list)
        # 有效字符串数据列表
        s_list_valid = list(eval(i[i.find(',') + 1:]) for i in s_list)
        
        # 测试
        #s_list_valid = list(list(int(y/10) for y in x) for x in s_list_valid)
        
        # 校验每个列表内对象的数据个数是否是二的整数倍
        for x in s_list_valid:
            if (len(x) % 2) != 0:
                print('error: ', x)
                return None
        
        # 校验每个列表内对象的长度是否相等
        if __list_comparison_func(tuple(s_list_valid), len) == False:
            print('error: data length error')
            return None            

        coordinate_list = list( list(__coordinates(x[y], x[y + 1]) for y in range(0, len(x), 2)) for x in s_list_valid )
        length_list = list( max( list(x[y] for y in range(0, len(x), 2)) ) - min( list(x[y] for y in range(0, len(x), 2)) ) for x in s_list_valid )
        breadth_list = list( max( list(x[y] for y in range(1, len(x), 2)) ) - min( list(x[y] for y in range(1, len(x), 2)) ) for x in s_list_valid )
        area = list(map(lambda x, y : x * y, length_list, breadth_list))

        rectangle_list = list(map(__rectangle, s_list_invalid, coordinate_list, length_list, breadth_list, area))
        rectangle_list.sort(reverse = False, key = (lambda x: x.area))   
        
        return rectangle_list
    except Exception as e:
        traceback.print_exc()
        return None
# rectangle转全部line数据
def rectangle_turn_all_line(l: tuple = None):
    '''
    函数作用：
        rectangle 转 [line] 数据
    参数：
        l: class rectangle
    return: 
        [class line] or None    
    '''
    try:
        if l == None:
            return None
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x)
        max_x = float(l.coordinates_list[0].x + l.length)
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y)
        max_y = float(l.coordinates_list[0].y + l.breadth)
        
        return {
            'min_y' : __line(min_coordinates = __coordinates(min_x, min_y), max_coordinates = __coordinates(max_x, min_y),  line_slope = 0.0),
            'max_y' : __line(min_coordinates = __coordinates(min_x, max_y), max_coordinates = __coordinates(max_x, max_y),  line_slope = 0.0)
        }
    except Exception as e:
        traceback.print_exc()  
        return None    
# rectangle转周长的集合(四条边 line)
def rectangle_turn_perimeter(l: tuple = None):
    '''
    函数作用：
        rectangle转周长的集合(四条边 line)
    参数：
        l: class rectangle
    return: 
        {key:class line} or None    
    '''
    try:
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.x))
        min_x = float(l.coordinates_list[0].x)
        max_x = float(l.coordinates_list[0].x + l.length)
        
        l.coordinates_list.sort(reverse = False, key = (lambda i: i.y))
        min_y = float(l.coordinates_list[0].y)
        max_y = float(l.coordinates_list[0].y + l.breadth)

        # x 下 上
        line_2 = __line(min_coordinates = __coordinates(min_x, min_y), max_coordinates = __coordinates(max_x, min_y),  line_slope = __calculate_slope_angle(__coordinates(min_x, min_y), __coordinates(max_x, min_y)))
        line_1 = __line(min_coordinates = __coordinates(min_x, max_y), max_coordinates = __coordinates(max_x, max_y),  line_slope = __calculate_slope_angle(__coordinates(min_x, max_y), __coordinates(max_x, max_y)))
        # y 左 右
        line_3 = __line(min_coordinates = __coordinates(min_x, min_y), max_coordinates = __coordinates(min_x, max_y),  line_slope = __calculate_slope_angle(__coordinates(min_x, min_y), __coordinates(min_x, max_y)))
        line_4 = __line(min_coordinates = __coordinates(max_x, min_y), max_coordinates = __coordinates(max_x, max_y),  line_slope = __calculate_slope_angle(__coordinates(max_x, min_y), __coordinates(max_x, max_y)))
        return {'up': line_1, 'down': line_2, 'left': line_3, 'right': line_4}
    except Exception as e:
        traceback.print_exc()  
        return None        

# 根据线段添加连接线段和描述框(矩形)
def judging_line_and_all_line_return_describe_rectangle(line: tuple = None, rectangle_all_line: list = None, 
                                                        line_all_line: tuple = None, length: float = 0, 
                                                        breadth: float = 0, line_length: float = 0,
                                                        angle: float = 0
                                                        ):
    '''
    函数作用：
        用line线段点的集合做初始点射出一条线段，线段的角度为angle长度为line_length，在线段的终点做矩形，矩形长度为length，宽度为breadth
    参数：
        line: 线段 (class line)
        all_line_list: 全部矩形线段 (list class line)
        line_all_line: 全部单独线段 (list class line)
        length: 长度(length>0)
        breadth: 宽度(breadth>0)
        line_length: 线段长度(line_length>0)
        angle: 角度 (0 <= angle <= 720)
        interval: interval 生成矩形的间隔
    return: 
        describe_rectangle or None
    '''

    try:
        examine_dict_greater_than_zero  = lambda x: False if x >= 0.0 else True
        determine_vertical = lambda i: True if math.isclose(90.0, i, rel_tol = 1e-6) or math.isclose(270.0, i, rel_tol = 1e-6) else False
        
        if examine_dict_greater_than_zero(length):
            return None
        if examine_dict_greater_than_zero(breadth):
            return None   
        if examine_dict_greater_than_zero(line_length):
            return None
        if not(0.0 <= angle and angle <= 720.0):
            return None 
        
        coordinates_xy = __reutrn_line_coordinates_collection(line) 
        
        for i in coordinates_xy:
            
            line = __line_generate(i, angle, line_length)
            line_x_min = line.min_coordinates.x
            line_x_max = line.max_coordinates.x

            value_domain_intersections = None
            line_value_domain_intersections = None
            # 获取定义域与线段有交集的矩形
            filtration_rectangle_domain = list({'line': x, 'x_intersections': __intersections_of_two_tuples(__assemble(line_x_min, line_x_max), __assemble(x['min_y'].min_coordinates.x, x['min_y'].max_coordinates.x)) } for x in rectangle_all_line if __intersections_of_two_tuples(__assemble(line_x_min, line_x_max), __assemble(x['min_y'].min_coordinates.x, x['min_y'].max_coordinates.x)) != None )
            # 判断线段与线段相交，方法同上
            line_filtration_rectangle_domain = list({'line': x, 'x_intersections': __intersections_of_two_tuples(__assemble(line_x_min, line_x_max), __assemble(x.min_coordinates.x, x.max_coordinates.x)) } for x in line_all_line if __intersections_of_two_tuples(__assemble(line_x_min, line_x_max), __assemble(x.min_coordinates.x, x.max_coordinates.x)) != None )
            
            # 判断线段值域和矩形值域
            for x in filtration_rectangle_domain:
                if determine_vertical(angle):
                    value_domain_intersections = __intersections_of_two_tuples(__line_func(line, x['x_intersections'].min), __assemble(x['line']['min_y'].min_coordinates.y, x['line']['max_y'].max_coordinates.y)) 
                else:
                    value_domain_intersections = __intersections_of_two_tuples(__assemble(__line_func(line, x['x_intersections'].min), __line_func(line, x['x_intersections'].max)), __assemble(x['line']['min_y'].min_coordinates.y, x['line']['max_y'].max_coordinates.y))

                if value_domain_intersections != None:
                    break
            
            if value_domain_intersections != None:
                continue
            
            # 判断线段值域和其他全部线段值域
            for x in line_filtration_rectangle_domain:
                
                if determine_vertical(angle) and not(determine_vertical(x['line'].line_slope)):
                    line_value_domain_intersections = __intersections_of_two_tuples(__line_func(line, x['x_intersections'].min), __assemble(__line_func(x['line'], x['x_intersections'].min), __line_func(x['line'], x['x_intersections'].max)))
                elif not(determine_vertical(angle)) and determine_vertical(x['line'].line_slope):
                    line_value_domain_intersections = __intersections_of_two_tuples(__assemble(__line_func(line, x['x_intersections'].min), __line_func(line, x['x_intersections'].max)), __line_func(x['line'], x['x_intersections'].min))
                elif determine_vertical(angle) and determine_vertical(x['line'].line_slope):
                    line_value_domain_intersections = __intersections_of_two_tuples(__line_func(line, x['x_intersections'].min), __line_func(x['line'], x['x_intersections'].min))
                else:
                    line_value_domain_intersections = __intersections_of_two_tuples(__assemble(__line_func(line, x['x_intersections'].min), __line_func(line, x['x_intersections'].max)), __assemble(__line_func(x['line'], x['x_intersections'].min), __line_func(x['line'], x['x_intersections'].max)))
            
                if line_value_domain_intersections != None:
                    break
            
            if value_domain_intersections == None and line_value_domain_intersections == None:
                x_list = [line.min_coordinates.x, line.max_coordinates.x]
                y_list = [line.min_coordinates.y, line.max_coordinates.y]
                x_list.remove(i.x)
                y_list.remove(i.y)
                
                if angle > 360.0:
                    angle = angle - 360.0
            
                if 0.0 < angle and angle <= 90.0:
                    min_x = x_list[0]
                    min_y = y_list[0]     
                    description = __describe_rectangle('0', [__coordinates(min_x + length, min_y + breadth), __coordinates(min_x, min_y + breadth), __coordinates(min_x + length, min_y), __coordinates(min_x, min_y)], length, breadth, length * breadth, line)                                                    
                elif 90.0 < angle and angle <= 180.0:
                    min_x = x_list[0] - length
                    min_y = y_list[0]     
                    description = __describe_rectangle('0', [__coordinates(min_x + length, min_y + breadth), __coordinates(min_x, min_y + breadth), __coordinates(min_x + length, min_y), __coordinates(min_x, min_y)], length, breadth, length * breadth, line)                                                    
                elif 180.0 < angle and angle <= 270.0:
                    min_x = x_list[0] - length
                    min_y = y_list[0] - breadth   
                    description = __describe_rectangle('0', [__coordinates(min_x + length, min_y + breadth), __coordinates(min_x, min_y + breadth), __coordinates(min_x + length, min_y), __coordinates(min_x, min_y)], length, breadth, length * breadth, line)                                                    
                elif 270.0 < angle and angle <= 360.0 or math.isclose(0.0, angle, abs_tol = 1e-6):
                    min_x = x_list[0]
                    min_y = y_list[0] - breadth   
                    description = __describe_rectangle('0', [__coordinates(min_x + length, min_y + breadth), __coordinates(min_x, min_y + breadth), __coordinates(min_x + length, min_y), __coordinates(min_x, min_y)], length, breadth, length * breadth, line)                                                    
                                                                    
                line_description = rectangle_turn_all_line(description)
                description_x_min = description.coordinates_list[0].x
                description_x_max = description_x_min + description.length
                description_y_min = description.coordinates_list[0].y
                description_y_max = description_y_min + description.breadth
                
                # 把新生成的描述框(矩形)再重新和所有矩形和线段比较一遍，方法和上面的一样
                filtration_description_domain = list({'line': x, 'x_intersections': __intersections_of_two_tuples(__assemble(description_x_min, description_x_max), __assemble(x['min_y'].min_coordinates.x, x['min_y'].max_coordinates.x))} for x in rectangle_all_line if __intersections_of_two_tuples(__assemble(description_x_min, description_x_max), __assemble(x['min_y'].min_coordinates.x, x['min_y'].max_coordinates.x)) != None )
                line_filtration_description_domain = list({'line': x, 'x_intersections': __intersections_of_two_tuples(__assemble(description_x_min, description_x_max), __assemble(x.min_coordinates.x, x.max_coordinates.x)) } for x in line_all_line if __intersections_of_two_tuples(__assemble(description_x_min, description_x_max), __assemble(x.min_coordinates.x, x.max_coordinates.x)) != None )
                r_intersections = None
                line_intersections = None
                
                for x in filtration_description_domain:
                    r_intersections = __intersections_of_two_tuples(__assemble(description_y_min, description_y_max), __assemble(x['line']['min_y'].min_coordinates.y, x['line']['max_y'].max_coordinates.y))
                    if r_intersections != None:
                        break
                    
                if r_intersections != None:
                    continue       
                           
                for x in line_filtration_description_domain:
                    if determine_vertical(x['line'].line_slope):
                        line_intersections = __intersections_of_two_tuples(__assemble(description_y_min, description_y_max), __line_func(x['line'], x['x_intersections'].min)) 
                    else:
                        line_intersections = __intersections_of_two_tuples(__assemble(description_y_min, description_y_max), __assemble(__line_func(x['line'], x['x_intersections'].min), __line_func(x['line'], x['x_intersections'].max)))

                    if line_intersections != None:
                        break                       
                    
                if r_intersections == None and line_intersections == None:
                    return description     

        
        return None  
                
    except Exception as e:
        traceback.print_exc()  
        return None 
    pass

# 循环judging_line_and_all_line_return_describe_rectangle
def loop_judging_line_and_all_line_return_describe_rectangle(rectangle_describe_list: tuple = None, describe_length: float = 0, 
                                                        describe_breadth: float = 0, line_length: float = 0,
                                                        angle: float = 0, rectangle_and_describe_interval: float = 0,
                                                        describe_and_describe_interval: float = 0
                                                        ):
    '''
    函数作用：
        循环judging_line_and_all_line_return_describe_rectangle
    参数：
        rectangle_describe_list: [{'rectangle':x, 'describe_list':list()]
        describe_length: 描述框长度(length>0)
        describe_breadth: 描述框宽度(breadth>0)
        line_length: 线段长度(line_length>0)
        angle: 角度 (0 <= angle <= 720)
        rectangle_and_describe_interval: 矩形和描述框的间隔
        describe_and_describe_interval: 描述框和描述框的间隔
    return: 
        [{'rectangle':x, 'describe_list':list()] or none
    '''    
    try:
        examine_dict_greater_than_zero = lambda x: False if x >= 0.0 else True

        if examine_dict_greater_than_zero(describe_length):
            return None
        if examine_dict_greater_than_zero(describe_breadth):
            return None   
        if examine_dict_greater_than_zero(line_length):
            return None
        if not(0.0 <= angle and angle <= 720.0):
            return None         
        
        r_list = rectangle_describe_list.copy()
        r_modify_list = rectangle_describe_list.copy()
    
        dict_angle = {}
        dict_angle['up'] = angle
        dict_angle['left'] = 90.0 + angle
        dict_angle['down'] = angle + 180.0
        dict_angle['right'] = 270.0 + angle
        # 'rectangle':
        r_modify_list = list({'rectangle': modify_rectangle_min_domain_of_definition(x['rectangle'], -rectangle_and_describe_interval), 'describe_list': list()} for x in r_modify_list )
        r_modify_list = list({'rectangle': modify_rectangle_max_domain_of_definition(x['rectangle'], rectangle_and_describe_interval), 'describe_list': list()} for x in r_modify_list )
        r_modify_list = list({'rectangle': modify_rectangle_min_value_domain(x['rectangle'], -rectangle_and_describe_interval), 'describe_list': list()} for x in r_modify_list )
        r_modify_list = list({'rectangle': modify_rectangle_max_value_domain(x['rectangle'], rectangle_and_describe_interval), 'describe_list': list()} for x in r_modify_list )        
        
        rectangle_all_line = list(rectangle_turn_all_line(x['rectangle']) for x in r_modify_list) + list(rectangle_turn_all_line(y) for x in r_modify_list for y in x['describe_list'] )
        line_all_line = list(y.line for x in r_modify_list for y in x['describe_list'] )
        
        for u, v in zip(r_list, r_modify_list):
            
            if len(u['describe_list']) > 0:
                continue 
            
            if v['rectangle'] == None or u['rectangle'].area < 0.0 or math.isclose(0.0, u['rectangle'].area, abs_tol = 1e-6):
                continue
            
            # 把矩形定义域值域最大最小值都加 -0.01
            modify_rectangle = modify_rectangle_value_domain_and_domain_of_definition(u['rectangle'], -0.005)
            # 获得原始rectangle 线段数据
            original_rectangle_line = rectangle_turn_all_line(v['rectangle'])
            # 修改过后的矩形线段
            modify_rectangle_line = rectangle_turn_all_line(modify_rectangle)   
            # 未修改的矩形的最外围四条边(周长)
            rectangle_perimeter = rectangle_turn_perimeter(u['rectangle'])
            
            # 把原始的矩形线段数据从全部矩形线段中删除
            if original_rectangle_line in rectangle_all_line:
                rectangle_all_line.remove(original_rectangle_line)
            
            # 添加修过过的矩形到全部矩形线段中
            if modify_rectangle_line != None:
                rectangle_all_line.append(modify_rectangle_line)                      

            for n in ['up', 'down', 'left', 'right']:
                describe_rectangle = judging_line_and_all_line_return_describe_rectangle(rectangle_perimeter[n], rectangle_all_line, line_all_line, describe_length, describe_breadth, line_length, dict_angle[n]) 
                if describe_rectangle != None:
                    u['describe_list'].append(describe_rectangle)
                    modify_describe_rectangle = modify_rectangle_value_domain_and_domain_of_definition(describe_rectangle, describe_and_describe_interval)
                    all_line_modify_describe_rectangle = rectangle_turn_all_line(modify_describe_rectangle)
                    rectangle_all_line.append(all_line_modify_describe_rectangle)
                    line_all_line.append(describe_rectangle.line)                  
                    break
            
            # 还原
            if modify_rectangle_line in rectangle_all_line:
                rectangle_all_line.remove(modify_rectangle_line)
            
            if original_rectangle_line != None:
                rectangle_all_line.append(original_rectangle_line)            
            
        return r_list
    
    except Exception as e:
        traceback.print_exc()  
        return None     
    
    
    pass

# matplotlib绘制矩形和线段，坐标系为像素坐标
def matplotlib_draw(rectangle_list: list = None, describe_list: list = None, x_coordinates_length: int = 40000, y_coordinates_length: int = 30000):
    '''
    函数作用：
        matplotlib绘制矩形和线段，坐标系为像素坐标
    参数：
        rectangle_list: [class rectangle]
        describe_list: [class describe_rectangle]
        x_coordinates_length: x 坐标轴长度
        y_coordinates_length: y 坐标轴长度
    return: 
        None
    '''    
    try:
        # 取出矩形列表和描述框列表
        line_list = list(x.line for x in describe_list)
        # 创建矩形绘制对象 左下起点，长，宽，颜色，α
        # 红色的是描述框 蓝色的是被描述对象
        rect_rectangle = list( plt.Rectangle(tuple( ( min( list(i.x for i in x.coordinates_list)), min(list(i.y for i in x.coordinates_list)) ) ), x.length, x.breadth, linewidth = 0.5, edgecolor='b', facecolor='none') for x in rectangle_list )
        rect_describe = list( plt.Rectangle(tuple( ( min( list(i.x for i in x.coordinates_list)), min(list(i.y for i in x.coordinates_list)) ) ), x.length, x.breadth, linewidth = 0.5, edgecolor='r', facecolor='none') for x in describe_list )
        
        # 绘制
        fig = plt.figure(figsize=(16, 9), dpi = 200)
        ax = fig.add_subplot(111)
        # 填充矩形
        for x in rect_rectangle:
            ax.add_patch(x)
        for x in rect_describe:
            ax.add_patch(x)
        
        # 填充线段
        for x in line_list:
            new_x = (x.min_coordinates.x, x.max_coordinates.x)
            new_y = (x.min_coordinates.y, x.max_coordinates.y)
            ax.add_line(Line2D( new_x, new_y, linewidth = 0.5, color = 'violet'))
        
        plt.xlim((0, x_coordinates_length))
        plt.ylim((y_coordinates_length, 0))
        plt.show()
        return None      
    except Exception as e:
        traceback.print_exc()  
        return None 
 
# 将__rectangle and __describe_rectangle 转为字典数据
def rectangle_data_turn_dict(rectangle: tuple = None):
    '''
    函数作用：
        将__rectangle and __describe_rectangle 转为字典数据
    参数：
        rectangle: class __rectangle and __describe_rectangle
    return: 
        dict or None    
    '''    
    try:
        dict_data = rectangle._asdict()
        coordinates_list = list()
        for x in dict_data['coordinates_list']:
            coordinates_list.append(x._asdict())
        
        rectangle_dict = dict()
        rectangle_dict['line_invalid_data'] = dict_data['line_invalid_data']
        rectangle_dict['length'] = dict_data['length']
        rectangle_dict['breadth'] = dict_data['breadth']
        rectangle_dict['area'] = dict_data['area']
        rectangle_dict['coordinates_list'] = coordinates_list

        if dict_data.__contains__("line") == True:
            rectangle_dict['line'] = line_data_turn_dict(dict_data['line'])
        
        return rectangle_dict
    except Exception as e:
        traceback.print_exc()  
        return None    

# 将__line 转为字典数据
def line_data_turn_dict(line: tuple = None):
    '''
    函数作用：
        将__line 转为字典数据
    参数：
        rectangle: class __line
    return: 
        dict or None    
    '''    
    try:
        dict_data = line._asdict()
        line_dict = dict()

        line_dict['line_slope'] = dict_data['line_slope']
        line_dict['max_coordinates'] = dict_data['max_coordinates']._asdict()
        line_dict['min_coordinates'] = dict_data['min_coordinates']._asdict()
        
        return line_dict
    except Exception as e:
        traceback.print_exc()  
        return None    
        
   
if __name__ == "pixel_graphics":
    __init()
	
	
	