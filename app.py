from pydoc import render_doc
from flask import Flask, redirect, render_template, request, send_from_directory
from openpyxl import Workbook ,styles, worksheet , load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.utils import get_column_letter
from excel import person, nums, make_excel
import sys,os

app = Flask(__name__)


@app.route("/")
def getindex():
    return render_template("index.html")

@app.route("/inherit")
def get_inherit():
    return render_template("inherit.html")

@app.route("/generate", methods=["POST"])
def get_excel():
    if request.method == "POST":
        f = request.form.to_dict()
        number = int(len(f) / 8)

        d = dict() ## 
        l = list() ## 存放所有name 當 dict的索引
        gen = list() ## 存放每筆資料的 gen
        for i in range(number):
            n = i + 1
            objectname = request.form.get('name'+ str(n))
            bday = request.form.get('bday' + str(n))
            dday = request.form.get('dday' + str(n))
            d[objectname] = person(request.form.get('check'+ str(n)), bday , dday ,request.form.get('wife'+ str(n)),request.form.get('parent'+ str(n)),request.form.get('id'+ str(n)),request.form.get('call'+ str(n)))
            l.append(objectname)

        

        for x in range(len(l)):
            gen.append(gen_count(d, l[x])) # 取得gen 資料
            # 計算後代數量 = 小孩數 + 小孩的配偶數
            if (d[l[x]].parent != ""):
                name = d[l[x]].parent
                d[name].soncount = d[name].soncount + 1 
            if (d[l[x]].wife != ""):
                name = d[l[x]].parent
                wife_n = d[l[x]].wife.split(',')
                d[name].soncount = d[name].soncount + len(wife_n)
        
        make_excel(d, l, app, gen)

        #     son = d[l[x]].son.split(',')
        #     wife_n = d[l[x]].wife.split(',')
        #     print(son[0],file=sys.stderr)
            # gen_count = 0 ## 幾代計算
            # d[l[x]].gen_set(1)
            # print(d[l[x]].gen,file=sys.stderr)
        

        ## 下載功能 line67  
        ## return send_from_directory('xlsx',filename, as_attachment=True)

        ## d dict 儲存 所有輸入資料 每個key內儲存一個class person key 從0開始 TODO:子女很多個?, name 當作 dict 的key        
                
    
    return redirect('/')

def gen_count(d, name):
    if (d[name].parent != ""):
        return 1 + gen_count(d, d[name].parent)
    else:
        return 1
        
        
if __name__ == '__main__':
    app.debug = True
    app.run()