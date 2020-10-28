# socket-chatroom

# 網路概論 作業2

請將本專案中的 server_new.py 增添繼承於Thread的物件類別 (class) Command

```python
class Command(threading.Thread):
    def __init__(self):
        super().__init__()
    
    ....
```

並在 run 方法 (method) 中置入 input 於無限迴圈中 
使得字串是`/quit`之時可以中斷所有連線並結束程式

```python
def run(self):
    while True:
        ipt = input()
        if ipt == '/quit':
            .....
```

