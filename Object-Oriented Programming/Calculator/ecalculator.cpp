#include "ecalculator.h"
#include "ui_ecalculator.h"
#include<string>

using namespace std;

Ecalculator::Ecalculator(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Ecalculator)
{
    ui->setupUi(this);
    ui->Button_clear->setIconSize(QSize(32,32));
    ui->Button_clear->setIcon(QIcon(":/image/image/trash.png"));
    m_opr.push(make_unique<Hash>());
    m_cheopr.push(make_unique<Hash>());
}

Ecalculator::~Ecalculator()
{
    delete ui;
}

QString get_formec(double result){    //设置最大输出长度
    QString rhs;
    int outputlength = 4;
    int inresult = int(result);
    double temp =inresult-result;
    if(abs(temp)<1.0e-6){
        result = int(result);
        rhs = QString::number(result,10,0);
    }
    else{
        rhs = QString::number(result,10,outputlength);
    }
    return rhs;
}

double Ecalculator::readNum(string::const_iterator& it) {
    string t;
    while (isNum(it)) {
        t.push_back(*it++);
    }
    return stod(t);
}

string Ecalculator::readStr(string::const_iterator& it) {
    string t;
    while (isStr(it)) {
        t.push_back(*it++);
    }
    return t;
}

string Ecalculator::readOpr(string::const_iterator& it) {
    string oo;
    while (isOpr(it)) {
        if (*it != '=')
            oo.push_back(*it++);
        else
            break;
    }
    return oo;
}

void Ecalculator::calculate() {			//添加异常处理
    double a[2] = { 0 };
    try {
        for (auto i = 0; i < m_opr.top()->numOprand(); ++i) {
            a[i] = m_num.top();
            m_num.pop();
        }
        m_num.push(m_opr.top()->get(a[1], a[0]));
    }  catch (const char* str) {
        throw str;
    }
    m_opr.pop();
}

double Ecalculator::doIt(const string& exp) {
    bool is_negative = 0;			//1表示下一个数是负数存入数堆栈
    bool nonumber = 1;
    for (auto it = exp.begin(); it != exp.end();) {
        if (isNum(it)){
            nonumber = 0;
            if (is_negative == 1) {
                m_num.push((-1) * readNum(it));
                is_negative = 0;
            }
            else
                m_num.push(readNum(it));
        }
        else {
            unique_ptr<Operator> oo;
            if (isStr(it)) {
                string f = readStr(it);
                if (f == "pi") {
                    m_num.push(PIe);
                }
                else if (f == "e") {
                    m_num.push(ee);
                }
                else if (f == "ans") {
                    m_num.push(anse);
                }
                else{
                    try {
                        auto oo = Factory::create_fun(f);
                    }
                    catch (const char* str) {
                        throw str;
                    }
                    auto oo = Factory::create_fun(f);
                    m_opr.push(std::move(oo));
                }

            }
            else if (isOpr(it)) {
                string o;
                o.push_back(*it++);
                if (o == "(")
                    nonumber = 1;
                try {
                    auto oo = Factory::create_opr(o);
                }
                catch (const char* str) {
                    throw str;
                }
                auto oo = Factory::create_opr(o);
                if ((oo->symbol() == "-" && m_opr.top()->symbol() == "#" && nonumber == 1) ||
                    (oo->symbol() == "-" && m_opr.top()->symbol() == "(" && nonumber == 1)) {
                    is_negative = 1;
                    continue;
                }

                while (oo->precedence() <= m_opr.top()->precedence()) {
                    if (m_opr.top()->symbol() == "#" || m_opr.top()->symbol() == "(")
                        break;
                    try {
                        calculate();
                    }
                    catch (const char* str) {								//跳出错误时需要对数据栈，操作符栈进行清空
                        throw str;
                    }
                }
                if (oo->symbol() == ")" && m_opr.top()->symbol() == "(") {
                    m_opr.pop();
                }
                if (oo->symbol() != "=" && oo->symbol() != ")")//右括号不进栈
                    m_opr.push(std::move(oo));
            }
            else {
                throw "Error: undefined behaviors!";
            }
        }
    }
    double result = m_num.top();
    m_num.pop();
    return result;
}

bool Ecalculator::del_space(string& exp)//自动删除空格并检查异常字符
{
    string res;
    for (auto it = exp.begin(); it != exp.end(); ++it) {
        if (isStr(it) || isNum(it) || isOpr(it))//符合语法
            res += *it;
        else if (*it == ' ') {}
        else {//不符合语法则抛出异常
            try {
                throw "Error:Unusual character!";
            }
            catch (const char* str) {
                throw str;
                return false;
            }
        }
    }
    exp = res;
    return true;
}

bool Ecalculator::bracheck(string& exp) {
    for (auto it = exp.begin(); it != exp.end(); ++it) {
        char o = *it;
        unique_ptr<Operator>oo;
        if (o == '(') {
            oo = make_unique<Lbra>();
            m_cheopr.push(std::move(oo));//加入专门用于存放括号的链栈
        }
        else if (o == ')' && m_cheopr.top()->symbol() == "(") {
            m_cheopr.pop();//右括号于左括号相匹配，弹出左括号
        }
        else if (o == ')' && m_cheopr.top()->symbol() == ")") {
            try {//栈顶为右括号说明未与左括号相消，语法错误
                throw "Error:Missing left bracket!";
            }
            catch (const char* str) {
                throw str;
                return false;
            }
        }
        else if (o == ')' && m_cheopr.top()->symbol() == "#") {
            try {//开始即输入右括号
                throw "Error:Missing left bracket!";
            }
            catch (const char* str) {
                throw str;
                return false;
            }
        }
    }
    if (m_cheopr.top()->symbol() == "(") {
        try {//最终有左括号遗留，输入括号不匹配
            throw "Error:Missing right bracket!";
        }
        catch (const char* str) {
            throw str;
            return false;
        }
    }
    else
        return (m_cheopr.top()->symbol() == "#");
}

bool Ecalculator::check(string& exp) {
    bool isvalid = 1;
    for (auto it = exp.begin(); it != exp.end(); ) {
        if (isOpr(it)) {
            string o = readOpr(it);//读入连续运算符
            size_t length = o.size();
            unique_ptr<Operator>oo;
            if (length == 2) {//连续运算符长度为二，要排除左括号与负数标志的组合
                if (o.at(1) == '(')
                    continue;
                else if (o == "(-")
                    continue;
                else if (o == "))")
                    continue;
                else if(o.at(0) == ')' )
                    continue;
                else {
                    isvalid = 0;
                    break;
                }
            }
            else if (length == 3) {//连续运算符长度为三，要排除左括号与负数标志的组合
                if (o.at(1) == '(' && o.at(2) == '-')
                    continue;
                else if(o.at(1) == '('&&o.at(2)=='(')
                    continue;
                else if(o.at(0)==')'&&o.at(1)==')')
                    continue;
                else {
                    isvalid = 0;
                    break;
                }
            }
            else if (length > 3)//长度过长不给予判断
            {
                isvalid = 1;
                break;
            }
            if (*it == '=')
                it++;
        }
        else
            it++;
    }
    if (isvalid == 0) {
        try {
            throw "Error:syntax errors!";
        }
        catch (const char* str) {
            throw str;
            return false;
        }
    }
    return isvalid;
}

void Ecalculator::on_Button_cal_clicked()
{
    QString inputexp = ui->lineEdit_input->text();
    string exp = inputexp.toStdString();
    if(inputexp.isEmpty()==0){
        string::iterator it = exp.end()-1;
        if(*it=='='){
            try {
                if (del_space(exp) && bracheck(exp)&& check(exp))
                    anse = doIt(exp);
                QString Inputnum = get_formec(anse);
                ui->label_outcome->setText(Inputnum);
            }  catch (const char* str) {
                QString Inputnum = QString::fromStdString(str);
                ui->label_outcome->setText(Inputnum);
            }
        }
        else{
            ui->label_outcome->setText("Please enter the equal sign");
        }
    }


}

void Ecalculator::on_Button_clear_clicked()
{
    QString input;
    ui->label_outcome->setText(input);
    ui->lineEdit_input->setText(input);
}

