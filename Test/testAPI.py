import jx3Data.jxDatas as JX3Data


def jx3school(school,shape):
    school_dict = JX3Data.school_number
    shape_dict = JX3Data.bodyType
    if school in school_dict:
        if shape in shape_dict:
            print("找到")


jx3school("七秀","萝")
