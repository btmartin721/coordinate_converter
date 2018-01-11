from math import modf

def convert_dms_2_dd(obj):
    if obj.dms_decimal:
        secdeci = obj.dms_seconds + "." + obj.dms_decimal
    else:
        secdeci = obj.dms_seconds

    sec = (float(secdeci) / (float(60)))
    min = ((float(obj.dms_minutes) + sec) / float(60))

    dd = (min + float(obj.dms_degrees))

    if obj.dms_sign == "negative":
        dd = (dd * -1)

    return dd

def convert_dms_2_ddm(obj):
    if obj.dms_decimal:
        secdeci = obj.dms_seconds + "." + obj.dms_decimal
    elif obj.dms_seconds:
        secdeci = obj.dms_seconds

    sec = (float(secdeci) / (float(60)))

    min = float(obj.dms_minutes) + sec

    if obj.dms_sign == "negative":
        ddm = str(obj.dms_degrees) + " " + str(min) + " " + obj.neg
    elif obj.dms_sign =="positive":
        ddm = str(obj.dms_degrees) + " " + str(min) + " " + obj.pos

    return ddm

def convert_ddm_2_dd(obj):
    mindec = obj.ddm_minutes + "." + obj.ddm_decimal
    min = ((float(mindec) / float(60)))
    dd = (float(obj.ddm_degrees) + min)

    if obj.ddm_sign == "negative":
        dd = (dd * -1)

    return dd

def convert_ddm_2_dms(obj):
    dcml_part = obj.ddm_decimal
    min = obj.ddm_minutes
    deg = obj.ddm_degrees

    tmp_sec = "0" + "." + str(dcml_part)

    sec = (60 * float(tmp_sec))

    if obj.ddm_sign == "negative":
        dms = str(deg) + " " + str(min) + " " + str("%.3f" % sec) + " " + obj.neg
    elif obj.ddm_sign == "positive":
        dms = str(deg) + " " + str(min) + " " + str("%.3f" % sec) + " " + obj.pos

    return dms

def convert_dd_2_dms(obj):
    dcml_part = obj.dd_decimal
    deg = obj.dd_degrees

    fltdcml = "0" + "." + str(dcml_part)

    tmp_min = (60 * float(fltdcml))
    tmp_sec, min = modf(tmp_min)
    sec = (60 * float(tmp_sec))
    min = int(min)

    dms = str(deg) + " " + str(min) + " " + str(sec)

    return dms

def convert_dd_2_ddm(obj):
    dcml_part = obj.dd_decimal
    deg = obj.dd_degrees

    fltdcml = "0" + "." + str(dcml_part)

    mindec = (60 * float(fltdcml))

    if obj.dd_sign == "negative":
        ddm = str(deg) + " " + str(mindec) + " " + obj.neg
    elif obj.dd_sign == "positive":
        ddm = str(deg) + " " + str(mindec) + " " + obj.pos

    return ddm

def get_dms_from_dms(obj):
    if obj.dms_decimal:
        if obj.dms_sign == "negative":
            dms = obj.dms_degrees + " " + obj.dms_minutes + " " + obj.dms_seconds + "." + obj.dms_decimal + " " + obj.neg
        elif obj.dms_sign == "positive":
            dms = obj.dms_degrees + " " + obj.dms_minutes + " " + obj.dms_seconds + "." + obj.dms_decimal + " " + obj.pos
    else:
        if obj.dms_sign == "negative":
            dms = obj.dms_degrees + " " + obj.dms_minutes + " " + obj.dms_seconds + " " + obj.neg
        elif obj.dms_sign == "positive":
            dms = obj.dms_degrees + " " + obj.dms_minutes + " " + obj.dms_seconds + " " + obj.pos


    return dms

def get_ddm_from_ddm(obj):
    if obj.ddm_sign == "negative":
        ddm = obj.ddm_degrees + " " + obj.ddm_minutes + "." + obj.ddm_decimal + " " + obj.neg
    elif obj.ddm_sign =="positive":
        ddm = obj.ddm_degrees + " " + obj.ddm_minutes + "." + obj.ddm_decimal + " " + obj.pos

    return ddm


def get_dd_from_dd(obj):
    dd = obj.dd_degrees + "." + obj.dd_decimal

    if obj.dd_sign == "negative":
        dd = (float(dd) * -1)

    return dd
