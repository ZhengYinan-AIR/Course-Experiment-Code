QT       += core gui
QT       +=  sql
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    addmessage.cpp \
    logwidget.cpp \
    main.cpp \
    managesystem.cpp

HEADERS += \
    addmessage.h \
    logwidget.h \
    managesystem.h

FORMS += \
    addmessage.ui \
    logwidget.ui \
    managesystem.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    r.qrc
