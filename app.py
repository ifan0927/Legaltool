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
        for i in range(number):
            n = i + 1
            objectname = request.form.get('name'+ str(n))
            bday = request.form.get('bday' + str(n))
            dday = request.form.get('dday' + str(n))
            d[objectname] = person(request.form.get('check'+ str(n)), bday , dday ,request.form.get('wife'+ str(n)),request.form.get('son'+ str(n)),request.form.get('id'+ str(n)),request.form.get('call'+ str(n)), 0)
            l.append(objectname)

        make_excel(l)


        #for x in range(len(l)):
        #     son_n = d[l[x]].son.split(',')
        #     wife_n = d[l[x]].wife.split(',')
        #     print(son_n[0],file=sys.stderr)
            # gen_count = 0 ## 幾代計算
            # d[l[x]].gen_set(1)
            # print(d[l[x]].gen,file=sys.stderr)
        # d[l[0]].draw(5,1, l[0])
        

        # ws0.column_dimensions['B'].width = 42
        # ws0.column_dimensions['C'].width = 14 
        # ws0.column_dimensions['E'].width = 13
        # ws0.column_dimensions['F'].width = 14
        # wb.save(app.root_path +'/xlsx/'+ filename)

        ## 下載功能 line67  
        ## return send_from_directory('xlsx',filename, as_attachment=True)

        ## d dict 儲存 所有輸入資料 每個key內儲存一個class person key 從0開始 TODO:子女很多個?, name 當作 dict 的key        
                
    
    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    app.run()