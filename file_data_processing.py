# coding = UTF-8

# 用只读的方式打开文件，单字节的方式读取并返回文件全部字节数据
def read_all_text(file_path: str = None, edg: str = 'UTF-8'):
    try:
        fp = open(file = file_path, mode = 'r', encoding = edg)
        d = fp.read()
    except IOError as e:      
        print(e.filename + " except IOError")
        return None
    except OSError as e:    
        print(e.filename + " except OSError")
        return None
    except:
        print("Unknown Error")
        return None
    finally:
        fp.close()

    return d

def save_data_text(file_path: str = None, edg: str = 'UTF-8', data: str = None):
    try:
        fp = open(file = file_path, mode = 'w', encoding = edg)
        d = fp.write(data)
    except IOError as e:      
        print(e.filename + " except IOError")
        return None
    except OSError as e:    
        print(e.filename + " except OSError")
        return None
    except:
        print("Unknown Error")
        return None
    finally:
        fp.close()

    return d

