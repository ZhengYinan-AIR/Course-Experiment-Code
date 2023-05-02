#include "calculator.h"
#include "ui_calculator.h"
#include <QApplication>
#include <string>
#include <iostream>

using namespace std;

// 使用宏对Operator进行注册
map<string, function<unique_ptr<Operator>()>> Factory::ms_operator; // 定义存储ObjectCreator的静态map
map<string, function<unique_ptr<Operator>()>> Factory::ms_function; // 定义存储ObjectCreator的静态map
REGISTRAROPR(Plus, "+");
REGISTRAROPR(Minus, "-");
REGISTRAROPR(Multiply, "*");
REGISTRAROPR(Divide, "/");
REGISTRAROPR(Lbra, "(");
REGISTRAROPR(Rbra, ")");
REGISTRAROPR(Equal, "=");
REGISTRAROPR(Power, "^");
REGISTRAROPR(Mod, "%");
REGISTRAROPR(Fac, "!");
REGISTRARFUN(Log, "log");
REGISTRARFUN(Ln, "ln");
REGISTRARFUN(Sin, "sin");
REGISTRARFUN(Cos, "cos");
REGISTRARFUN(Tan, "tan");
REGISTRARFUN(aSin, "asin");
REGISTRARFUN(aCos, "acos");
REGISTRARFUN(aTan, "atan");
REGISTRARFUN(dtor, "dtor");
REGISTRARFUN(rtod, "rtod");
REGISTRARFUN(Sqrt, "sqrt");
double ans ;
double anssc;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Calculator w;
    w.show();
    return a.exec();
}





