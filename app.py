from pydoc import render_doc
from flask import Flask, redirect, render_template, request, send_from_directory
from openpyxl import Workbook ,styles, worksheet , load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.utils import get_column_letter
import sys,os
app = Flask(__name__)
wb = Workbook()
ws0 = wb.create_sheet("繼承系統表",0)

## 全邊框
thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

filename = '繼承系統表.xlsx'

## excel內style設定
font_title = styles.Font(u'標楷體',size=16,bold=True)
font_context = styles.Font(u'標楷體',size=11)


def nums(first_number, last_number, step=1):
    return range(first_number, last_number+1, step)

class person:
    
    def __init__(self, check, bday , dday, wife, son, pid,call,gen):
        self.check = check
        self.bday = bday
        self.dday = dday
        self.wife = wife
        self.son = son
        self.pid = pid
        self.call = call
        self.gen = gen

    def gen_set(self, int):
        self.gen = int

    def draw (self, s_col,s_row,name):
        ws0.merge_cells(start_row = s_row + 1,start_column = s_col, end_row = s_row + 2, end_column= s_col)
        ws0.cell(row = s_row, column = s_col).fill = styles.PatternFill("solid", fgColor="000000")
        ws0.cell(row = s_row, column = s_col + 1).value = name
        ws0.cell(row = s_row + 1, column = s_col).value = self.call
        ws0.cell(row = s_row + 1, column = s_col + 1).value = self.bday
        ws0.cell(row = s_row + 2, column = s_col + 1).value = self.dday
        if (self.check == 1):
            ws0.cell(row = s_row + 3, column= s_col ).value = "有拋棄繼承"
        else: 
            ws0.cell(row = s_row + 3, column= s_col ).value = "無拋棄繼承"
        ws0.cell(row = s_row + 3, column= s_col + 1).value = self.pid
        for c in nums(s_col, s_col + 1):
            for r in nums(s_row , s_row + 3):
                ws0.cell(row= r , column=c).font  = font_context
                ws0.cell(row= r , column=c).alignment = styles.Alignment(horizontal="center",vertical='center')
                ws0.cell(row= r , column=c).border =  thin_border


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

        #excel檔內標題 字型/標題
        ws0.merge_cells('A1:C4') 
        ws0['A1'] = l[0] + "的繼承系統表"
        ws0.cell(row=1,column=1).alignment = styles.Alignment(horizontal="center",vertical='center') ## 置中對齊
        ws0.cell(row=1,column=1).font = font_title ##標題字形

        ws0['B5'] =  "表格範例"
        ws0.cell(row=5,column=2).alignment = styles.Alignment(horizontal="center",vertical='center')
        ws0.cell(row=5 , column=2).font  = font_context

        ##excel檔內範例 內容/字型/標題
        ws0.merge_cells("B7:B8")
        ws0['B6'] = '是否為繼承人,若為繼承人為此格為黑底'
        ws0['C6'] = '姓名'
        ws0['B7'] = '稱謂'
        ws0['C7'] = '出生日'
        ws0['C8'] = '死亡日'
        ws0['B9'] = '有無拋棄繼承'
        ws0['C9'] = '身分證字號'
        for r in nums(6,9):
            for c in nums(2,3):
                ws0.cell(row= r , column=c).font  = font_context
                ws0.cell(row= r , column=c).alignment = styles.Alignment(horizontal="center",vertical='center')
                ws0.cell(row= r , column=c).border =  thin_border


        #for x in range(len(l)):
        #     son_n = d[l[x]].son.split(',')
        #     wife_n = d[l[x]].wife.split(',')
        #     print(son_n[0],file=sys.stderr)
            # gen_count = 0 ## 幾代計算
            # d[l[x]].gen_set(1)
            # print(d[l[x]].gen,file=sys.stderr)
        d[l[0]].draw(5,1, l[0])
        

        ws0.column_dimensions['B'].width = 42
        ws0.column_dimensions['C'].width = 14 
        ws0.column_dimensions['E'].width = 13
        ws0.column_dimensions['F'].width = 14
        wb.save(app.root_path +'/xlsx/'+ filename)

        ## 下載功能 line67  
        ## return send_from_directory('xlsx',filename, as_attachment=True)

        ## d dict 儲存 所有輸入資料 每個key內儲存一個class person key 從0開始 TODO:子女很多個?, name 當作 dict 的key        
                
    
    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    app.run()