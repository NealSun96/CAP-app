# -*- coding: utf-8 -*-

import fnmatch
import os
import pandas as pd
import json
import pytz


def generate_student_excel(course):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, "*_STUDENTS_*.xlsx"):
            os.remove(file)

    excel_data = {u'姓名': [],
                   'email': [],
                   'BU': [],
                   'Feedback': [],
                   'Action Plan': [],
                   'Knowledge Test': [],
                   'Diagnosis': [],
                   u'具体Feedback结果': [],
                   u'具体Action Plan结果': [],
                   u'具体Diagnosis结果': [],
                   }
    for enroll in course.enrollment_set.all():
        if enroll.start_time != course.start_time:
            continue

        excel_data[u'姓名'].append(enroll.user.get_full_name())
        excel_data['email'].append(enroll.user.username)
        excel_data['BU'].append(enroll.user.groups.first().name if enroll.user.groups.first() else "N/A")
        if enroll.feedback_set.first():
            excel_data['Feedback'].append(u"已完成")
            feedbacks = json.loads(enroll.feedback_set.first().feedbacks)
            feedbacks = ['N/A' if not f else f for f in feedbacks]
            excel_data[u'具体Feedback结果'].append(u", ".join(feedbacks[:-1])+u"\n反馈："+feedbacks[-1])
        else:
            excel_data['Feedback'].append(u"未完成")
            excel_data[u'具体Feedback结果'].append("N/A")

        if enroll.actionplananswer_set.first():
            excel_data['Action Plan'].append(u"已完成")
            answers = json.loads(enroll.actionplananswer_set.first().answers)
            excel_data[u'具体Action Plan结果'].append(u"\n".join([str(a[0]+1)+u". "+a[1] for a in enumerate(answers)]))
        else:
            excel_data['Action Plan'].append(u"未完成")
            excel_data[u'具体Action Plan结果'].append("N/A")

        if enroll.knowledgetestanswer_set.first():
            nod = (enroll.knowledgetestanswer_set.first().completion_date - enroll.start_time).days
            excel_data['Knowledge Test'].append(u"%s天完成" % nod)
        else:
            excel_data['Knowledge Test'].append(u"未完成")

        if enroll.diagnosis_set.first():
            nod = (enroll.diagnosis_set.first().completion_date - enroll.start_time).days
            excel_data['Diagnosis'].append(u"%s天完成" % nod)

            diagnosis = u"自我诊断: %s\n共同诊断: %s\n" % (enroll.diagnosis_set.first().self_diagnosis,
                                                   enroll.diagnosis_set.first().other_diagnosis)
            ch_options = [u"没有变化", u"稍有改善", u"明显进步"]
            for option in enumerate(ch_options):
                diagnosis = diagnosis.replace(str(option[0]+1), option[1])
            excel_data[u'具体Diagnosis结果'].append(diagnosis)
        else:
            excel_data['Diagnosis'].append(u"未完成")
            excel_data[u'具体Diagnosis结果'].append("N/A")

    df = pd.DataFrame(excel_data)
    df = df[[u'姓名', 'email', 'BU', 'Feedback', 'Action Plan', 'Knowledge Test', 'Diagnosis', u'具体Feedback结果', u'具体Action Plan结果', u'具体Diagnosis结果']]
    df.set_index(u'姓名', inplace=True)
    filename = u'%s_STUDENTS_%s.xlsx' % (course.course_name, course.start_time.replace(tzinfo=pytz.utc).
                                   astimezone(pytz.timezone('Asia/Shanghai')).date())
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def generate_data_excel(course, data_list, titles, start_time, end_time):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, "*_DATA_*.xlsx"):
            os.remove(file)

    excel_data = {
        '': [u'Knowledge Test 统计人数', u'Knowledge Test 平均初次得分', u'Knowledge Test 平均最终得分',
             u'Knowledge Test 平均完成天数', u'Knowledge Test 平均完成秒数', u'Diagnosis 统计人数',
             u'Diagnosis 自我诊断明显进步比例（%）', u'Diagnosis 共同诊断明显进步比例（%）',
             u'Diagnosis 平均完成天数'],
        u'全部学员': data_list[0],
        "Cardio": [],
        "ENDO": [],
        "PION": [],
        "CRM": [],
        "EP": [],
        "Urology": [],
        "Structural Heart": [],
        "HK&TW": [],
        "Emerging Marketing": [],
        "Others": [],
        }

    for t in enumerate(titles):
        excel_data[t[1]] = data_list[t[0]+1]

    df = pd.DataFrame(excel_data)
    titles.insert(0, '')
    titles.insert(1, u'全部学员')
    df = df[titles]
    df.set_index('', inplace=True)
    filename = u'%s_DATA_%s_to_%s.xlsx' % (course.course_name, start_time[:10], end_time[:10])
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
