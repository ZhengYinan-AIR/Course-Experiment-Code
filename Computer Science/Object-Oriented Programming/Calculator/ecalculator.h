#ifndef ECALCULATOR_H
#define ECALCULATOR_H

#include <QDialog>

#include<memory>
#include<string>
#include<QString>
#include<cmath>
#include"Operator.h"
#include"OperatorFactory.h"
#include"Stack.h"

namespace Ui {
class Ecalculator;
}

constexpr double PIe = 3.14159265358979323846;
constexpr double ee = 2.718281828459045;

class Ecalculator : public QDialog
{
    Q_OBJECT
private:
    Stack<double> m_num;
    Stack<unique_ptr<Operator>> m_opr;
    Stack<unique_ptr<Operator>> m_cheopr;
    double readNum(string::const_iterator& it);
    bool isNum(string::const_iterator& it) {					//判断是否是数字
        return *it >= '0' && *it <= '9' || *it == '.';
    }
    string readStr(string::const_iterator& it);
    bool isStr(string::const_iterator& n) {						//判断是否是字符
        return *n >= 'a' && *n <= 'z';
    }
    bool isOpr(string::const_iterator& it) {					//判断是否是操作符
        string o;
        o.push_back(*it);
        for (auto is = Factory::ms_operator.begin(); is != Factory::ms_operator.end(); ++is) {
            if (is->first == o)
                return true;
        }
        return false;
    }
    string readOpr(string::const_iterator& it);					//读取连续运算符的最后一位
    void calculate();
public:
    double doIt(const string& exp);
    bool del_space(string& exp);//删除空格以及判断输入字符是否合法
    bool bracheck(string& exp);//括号检测
    bool check(string& exp);//检查语法是否合法（连续输入多个运算符，运算符顺序违法

public:
    explicit Ecalculator(QWidget *parent = nullptr);
    ~Ecalculator();

private slots:


    void on_Button_cal_clicked();

    void on_Button_clear_clicked();

private:
    Ui::Ecalculator *ui;
    double anse;
};

QString get_formec(double);

#endif // ECALCULATOR_H
