#coding:utf-8
# This is very scratchy and supports only limited portion of Python functions.
#%%
import ast
import math
import inspect

import dill

CONDITION = "condition"
OPERATION = "operation"
INPUTOUTPUT = "inputoutput"
PARALLEL = "parallel"
SUBROUTINE = "subroutine"
START = "start"
END = "end"
fnode_id = 0


class CodeflowVisitor(ast.NodeVisitor):
    def __init__(self, source):
        self._source = source  #源程序
        self._srclines = source.splitlines()  #源程序的行
        startnode = {
            "name": START,
            "type": START,
            "text": START,
            "yesno": None
        }
        self._fnodes = [startnode]  #流程图节点
        self._flines = []  # 流程图连线
        self._fstack = [startnode]  # 流程图节点的stack，用于记录未解决的节点
        super(ast.NodeVisitor).__init__()

    def _add_fnode(self, nodetype, text, stype=None, soption=None):
        # 加入节点, 其中stype表示语句的类型
        global fnode_id
        fnode_id += 1
        fnode = {
            "name": nodetype + str(fnode_id),
            "type": nodetype,
            "text": text,
            "stype": stype,
            "yesno": None
        }
        self._fnodes.append(fnode)

        # 加入线条
        lastnode = self._fstack.pop()  # 栈中的最后节点

        if stype == "for" or stype == "while" or stype == "if":  #循环语句，多推入一个节点，以便以后退出
            self._add_fline({
                "from": lastnode,
                "to": fnode,
                "yesno": lastnode["yesno"]
            })
            fnodeNO = fnode.copy()
            fnodeNO["yesno"] = "no"
            fnodeYES = fnode.copy()
            fnodeYES["yesno"] = "yes"
            self._fstack.append(fnodeNO)  #将该点入栈
            self._fstack.append(fnodeYES)
        else:
            self._add_fline({
                "from": lastnode,
                "to": fnode,
                "yesno": lastnode["yesno"]
            })
            self._fstack.append(fnode)  #将该点入栈

        return fnode

    def _add_fline(self, dict_fline):
        '''加入连线'''
        # 特殊处理多终点的情况
        _from = dict_fline["from"]
        _to = dict_fline["to"]
        if _from["type"] == CONDITION and _from["yesno"] == "terminal":
            for fnode in _from["terminal"]:
                yesno = fnode["yesno"]
                if yesno not in ["yes", "no"]:
                    yesno = None
                self._flines.append({"from": fnode, "to": _to, "yesno": yesno})
        #fline = {"from": _from, "to": _to, "yesno": yesno}
        else:
            self._flines.append(dict_fline)

    def _end_statement(self, stype, yesno=None):
        '''处理语句的结束'''

        if stype == "for" or stype == "while":
            lastnode = self._fstack.pop()  # 栈中的最后节点
            # 加入线条
            fornode = self._fstack[-1]  # 栈中多置入的判断节点
            lineyesno = lastnode["yesno"]
            if not lineyesno:
                lineyesno = "left"  #连回的线条走左边，效果好一点
            #else:
            #   lineyesno = lineyesno + ",left" #如果已有，绘图时会出问题

            self._add_fline({
                "from": lastnode,
                "to": fornode,
                "yesno": lineyesno
            })  #连回去
        elif stype == "if":
            if yesno == "terminal":
                ifnode = self._fstack[-1]
                ifnode["yesno"] = "terminal"  #将这个属性改掉，以方便后继节点与之相连
                return

            lastnode = self._fstack.pop()  # 栈中的最后节点
            ifnode = self._fstack[-1]
            # 记下终点
            if yesno == "yes" or yesno == "no":  # 将该终点并入到原if结点
                self._put_terminal_node(lastnode, ifnode)
            if yesno == "yes":
                self._fstack.append(ifnode)  #多置入一个if条件节点，以便后面相连

        elif stype == "prog":
            endnode = {"name": END, "type": END, "text": END}
            lastnode = self._fstack.pop()  # 栈中的最后节点， TODO:要考虑为if的情况
            self._fnodes.append(endnode)  #流程图节点
            self._add_fline({
                "from": lastnode,
                "to": endnode,
                "yesno": lastnode["yesno"]
            })  #连到结束

    def _put_terminal_node(self, lastnode, ifnode):
        if not "terminal" in ifnode:
            ifnode["terminal"] = []
        if lastnode["yesno"] != "terminal":
            ifnode["terminal"].append(lastnode)  #只是一个点
        else:
            ifnode["terminal"] += lastnode["terminal"]  #很多的点


    def _get_outter_node(self, stypes: list):
        '''得到该语句的外围的循环语句节点'''
        i = len(self._fstack) - 1
        while True:
            if self._fstack[i]["stype"] in stypes:
                break
            i -= 1
            if i < 0:
                return None #"没有找到相应的外围语句"
        return self._fstack[i]          
    
    def dovisit(self, with_explain=False):
        #文本描述
        str_text = self.visit(ast.parse(self._source))
        #生成流程图的文本
        self._end_statement("prog")  #加入结束节点
        str_flowchart = "\n"  #```flow
        for fnode in self._fnodes:
            str_flowchart += f'{fnode["name"]}=>{fnode["type"]}: {fnode["text"]}'
            if fnode["text"].startswith("for ") or fnode["text"].startswith(
                    "while "):
                str_flowchart += '|past'
            str_flowchart += '\n'
        for fline in self._flines:
            str_flowchart += f'{fline["from"]["name"]}'
            if fline["yesno"]:
                str_flowchart += f'({fline["yesno"]})'
            str_flowchart += f'->{fline["to"]["name"]}\n'
        str_flowchart += "\n"  #```
        return (str_text if with_explain else "") + str_flowchart

    def _parse_symbols(self, val: str) -> str:
        return val

    def get_node_source(self, node):
        if not node:
            return ""
        if isinstance(node, str):
            return node
        if not hasattr(node, "lineno"):
            return str(node)
        line0 = node.lineno - 1
        c0 = node.col_offset
        line1 = node.end_lineno - 1
        c1 = node.end_col_offset
        src = ""
        if line0 == line1:
            src = self._srclines[line0][c0:c1]
        else:
            scr = self._srclines[line0][c0] + "\n"
            for n in range(line0 + 1, line1):
                src += self._srclines[n] + "\n"
            src += self._srclines[line1][:c1]
        return src

    def generic_visit(self, node, addfnode=True):
        '''获得源码'''
        #if hasattr(node, "value"):
        #node = node.value  #针对Call
        if not hasattr(node, "lineno"):
            return str(node)

        src = self.get_node_source(node)

        if addfnode:
            ftype = OPERATION
            if "input(" in src or "print(" in src or "write(" in src or "read(" in src:
                ftype = INPUTOUTPUT
            self._add_fnode(ftype, src)

        return src

    def visit_Module(self, node):
        #return self.visit(node.body[0])  #模块实为包含当前函数的临时模块，body[0]即为当前函数
        s = ""
        for n in node.body:
            src = self.get_node_source(n)
            #if src.startswith("import dll") or src.startswith(
            #        "dill.loads"):  #有点特殊???
            #    continue
            s += self.visit(n)
        return s

    def visit_FunctionDef(self, node):
        name_str = r'函数 ' + str(node.name) + ' '
        arg_strs = [
            self._parse_symbols(str(arg.arg)) for arg in node.args.args
        ]  #参数

        body_str = ""
        for i in range(len(node.body)):
            body_str += " " + self.visit(node.body[i])
        return name_str + '(' + ', '.join(arg_strs) + r') 的流程： ' + body_str

    def visit_If(self, node):
        '''处理if语句，但elif还有点问题'''
        explain = r' 判断:'

        while isinstance(node, ast.If):  #循环处理多个if及elif
            #print("正在处理:", self.get_node_source(node))
            cond_str = self.generic_visit(node.test, addfnode=False)
            cfnode = self._add_fnode(CONDITION, "if " + cond_str, "if")
            true_str = ""
            for n in node.body:
                #print(self.get_node_source(n))
                true_str += " " + self.visit(n)
            self._end_statement("if", "yes")
            explain += r' 如果 ' + cond_str + r' 则 ' + true_str
            if node.orelse:
                node = node.orelse
                #这里有点诡异，其node.orelse[0]才是elif语句，这样下面的visit会递归调用，反而正确了？
            else:
                node = None
                break
        if node:
            #print("正在处理else语句:", self.get_node_source(node))
            false_str = ""
            if hasattr(node, '__iter__'):
                for n in node:
                    false_str += " " + self.visit(n)
            else:
                false_str += " " + self.visit(node)

            explain += r', 否则 ' + false_str
        else:
            #为了程序简单，没有else分支，强制加个pass分支
            self._add_fnode(OPERATION, "pass", "pass") 
            #cfnode2 = cfnode.copy()  # 主要是借用原节点的名字
            #cfnode2["yesno"] = "no"  # 增加一个no分支
            #self._fstack.append(cfnode2)
            #self._put_terminal_node(cfnode2, cfnode) #出口

        self._end_statement("if", "no")

        self._end_statement("if", "terminal")
        return explain

    def visit_For(self, node):
        try:
            varname = node.target.id  # 单变量
            if hasattr(node.iter, "func"):
                func = node.iter.func.id
                args = node.iter.args
                args = [self.visit(arg) for arg in args]
                str_for = "for " + varname + " in " + func + "(" + ", ".join(
                    args) + ")"
            else:
                str_for = "for " + varname + " in " + self.generic_visit(
                    node.iter, False)
        except:
            varname = self.get_node_source(node.target)  #可能是元组
            iter_str = self.get_node_source(node.iter)  #可能是Attribute
            str_for = "for " + varname + " in " + iter_str

        self._add_fnode(CONDITION, str_for, "for")
        str_body = " 执行 "
        for n in node.body:
            str_body = " " + self.visit(n)
        self._end_statement("for")
        return "循环: " + str_for + str_body

    def visit_While(self, node):
        cond_str = self.generic_visit(node.test, addfnode=False)
        cfnode = self._add_fnode(CONDITION, "while " + cond_str, "while")
        str_body = " 执行 "
        for n in node.body:
            str_body = " " + self.visit(n)
        self._end_statement("while")
        return "循环: while " + cond_str + str_body

    def visit_Break_notwork(self, node):   
        # 这个逻辑没有实现，似乎实现了，图与画不出来   
        fnode = self._add_fnode(OPERATION, "break", "break")
        #self._fstack.pop() #移除该节点        
        outter = self._get_outter_node(["for", "while"]) #找到外围的语句
        outter2 = outter.copy()  #借用原结点的名字
        outter["yesno"] = "no"  #出口

        self._put_terminal_node(fnode,  outter)
        return "break"

    def visit_Assign(self, node):
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) or isinstance(
                node.value, ast.Assign):
            #return self.visit_Call(node.value)
            return self.generic_visit(node.value)

        return self.generic_visit(node)

    def visit_Name(self, node):
        return node.id

    def visit_Pass(self, node):
        return self.generic_visit(node)

    def visit_Return(self, node):
        #return " 返回 " + self.visit(node.value)
        return self.generic_visit(node)


def get_flowchart(fn, with_explain=False):
    if isinstance(fn, str):
        source = fn
    else:
        try:
            source = inspect.getsource(fn)
        except Exception:
            # Maybe running on console.
            source = dill.source.getsource(fn)

    return CodeflowVisitor(source).dovisit(with_explain)


htmltemplate = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>py2flowchart</title>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/raphael/2.3.0/raphael.min.js"></script>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
		<script src="https://cdn.bootcdn.net/ajax/libs/flowchart/1.14.0/flowchart.min.js"></script>
    </head>
    <body>
        <div id="canvas"></div>
		<pre id="code"></pre>
		<script>
			code= `{flowchartcode}`;
			chart = flowchart.parse(code);
			chart.drawSVG('canvas', {});
			$("#code").html(code);
		</script>
    </body>
</html>
"""

def pyfile2flowchart(infile, outfile):
    with open(infile, encoding="utf-8") as f:
        src = f.read()
    flow = get_flowchart(src)
    content = htmltemplate.replace("{flowchartcode}", flow)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(content)


def with_flowchart(*args):
    class _CodeflowedFunction:
        def __init__(self, fn):
            self._fn = fn
            self._str = get_flowchart(fn)

        @property
        def __doc__(self):
            return self._fn.__doc__

        @__doc__.setter
        def __doc__(self, val):
            self._fn.__doc__ = val

        @property
        def __name__(self):
            return self._fn.__name__

        @__name__.setter
        def __name__(self, val):
            self._fn.__name__ = val

        def __call__(self, *args):
            return self._fn(*args)

        def __str__(self):
            return self._str

        def _repr_latex_(self):
            """Hooks into Jupyter notebook's display system."""
            return "```flow\n" + self._str + "\n```"

        def _repr_html_(self):
            """Hooks into Jupyter notebook's display system."""
            return "```flow\n" + self._str + "\n```"

    if len(args) == 1 and callable(args[0]):
        return _CodeflowedFunction(args[0])
    else:
        return lambda fn: _CodeflowedFunction(fn)



    

# %%
