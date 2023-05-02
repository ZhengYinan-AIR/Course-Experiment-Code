#ifndef CALCULATOR_H
#define CALCULATOR_H
#include<memory>
#include<string>
#include<cmath>
#include"Operator.h"
#include"OperatorFactory.h"
#include"Stack.h"


constexpr double PI = 3.14159265358979323846;
constexpr double e = 2.718281828459045;
extern double ans;

class Calculator {
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
	Calculator() { m_opr.push(make_unique<Hash>()); m_cheopr.push(make_unique<Hash>()); }
	double doIt(const string& exp);
	bool del_space(string& exp);//删除空格以及判断输入字符是否合法		
	bool bracheck(string& exp);//括号检测
	bool check(string& exp);//检查语法是否合法（连续输入多个运算符，运算符顺序违法
	
};





#endif // !CALCULATOR_H
