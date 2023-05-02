#include "managesystem.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ManageSystem w;
    //w.show();
    return a.exec();
}
