from PyQt6.QtGui import QRegularExpressionValidator, QDoubleValidator
from PyQt6.QtCore import QRegularExpression, QObject, QLocale


def ipValidator(lineEditWidget:QObject):
    ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
    ip_regex = QRegularExpression("^" + ip_range + "\\." + ip_range + "\\." + ip_range + "\\." + ip_range + "$")
    return QRegularExpressionValidator(ip_regex, lineEditWidget)

def longitudeValidator(lineEditWidget:QObject):
    lng_range = "(?:1[89]|1[0-7][0-9]|[0-9]{1,2})(?:.[0-9]{6})?"
    lng_regex = QRegularExpression("^" + lng_range + "$")
    return QRegularExpressionValidator(lng_regex, lineEditWidget)

def latitudeValidator(lineEditWidget:QObject):
    lat_range = "(?:8[0-9]|[0-8]?[0-9])(?:.[0-9]{6})"
    lat_regex = QRegularExpression("^" + lat_range + "$")
    return QRegularExpressionValidator(lat_regex, lineEditWidget)

def isEmptyValidation(value):
    return value != None



# class EmptyTextValidator (QValidator) :
#
#
# class IntValidator (QValidator):
#
#
# class DoubleValidator (QValidator):
