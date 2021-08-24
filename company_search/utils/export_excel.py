import datetime

import xlwt
from django.http import FileResponse

def file_iterator(filename, chuck_size=512):
    """
    将文件分块返回
    :param filename: 文件名称
    :param chuck_size: 块的大小，默认 512
    :return: 文件以可迭代对象的方式分块返回
    """
    with open(filename, "rb") as f:
        while True:
            c = f.read(chuck_size)
            if c:
                yield c
            else:
                break

def export_excel(queryset, headers, columns, filename='file_name', choices_fields_value=None):
    """
    通过传递进去的数据构建 Excel 文件，并且以数据流的返回返回文件
    :param queryset: 数据列表，通常为筛选后的结果。
    :param headers:
        Excel 的表头，以列表的方式传入。
        例如： ['ID', '姓名', '手机号', '金额变更', '变更后余额']
    :param columns:
        数据列的名称，以列表的方式传入。
        例如：['pk', 'customer__name', 'customer__mobile', 'amounts', 'current_amounts']
    :param filename: 返回文件的文件名，必须以 .xls 为后缀
    :param choices_fields_value:
        包含 choices 的字段。
        例如：{'status': [('1', '未到货'), ('2', '部分到货'), ('3', '已到货')]}
    :return:
    """
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("data")
    choice_fields_dict = dict()
    if choices_fields_value:
        for field, choices in choices_fields_value.items():
            choice_dict = dict()
            for c in choices:
                choice_dict[c[0]] = c[1]
            choice_fields_dict[field] = choice_dict
    for i, h in enumerate(headers):
        sheet.write(0, i, h)
    cols = 1
    for query in queryset.values(*columns):
        for i, k in enumerate(columns):
            v = query.get(k)
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(v, datetime.date):
                v = v.strftime('%Y-%m-%d')
            if k in choice_fields_dict:
                v_display = choice_fields_dict.get(k).get(v)
                if v_display:
                    v = v_display
            sheet.write(cols, i, v)
        cols += 1
    wb.save(filename)
    response = FileResponse(file_iterator(filename))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
