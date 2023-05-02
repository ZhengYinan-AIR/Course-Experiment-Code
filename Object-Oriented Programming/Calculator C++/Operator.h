#ifndef OPERATOR_H
#define OPERATOR_H

#include<iostream>
#include<cmath>
#include<vector>

using namespace std;

//const vector<char>Opt_set = { '+','-','*','/','(',')','=','^','%' };	试用符号工厂后不再需要

class Operator {
protected:
	const string m_symbol;
	const int m_numberOprand;
	const int m_precedence;


public:
	Operator(string c, int numOprd, int pre) :m_symbol(c), m_numberOprand(numOprd), m_precedence(pre) {}
	string symbol() const { return m_symbol; }
	int numOprand() const { return m_numberOprand; }
	int precedence() const { return m_precedence; }
	virtual double get(double a, double b) const = 0;
	virtual ~Operator() {}
};

class Lbra :public Operator {
public:
	Lbra() :Operator("(", 1, 6) {}
	double get(double a, double b) const {
		return b;
	}
};

class Rbra :public Operator {
public:
	Rbra() :Operator(")", 1, 0) {}
	double get(double a, double b) const {
		return a;
	}
};

class Plus : public Operator {
public:
	Plus() :Operator("+", 2, 2) {}
	double get(double a, double b) const {
		return a + b;
	}
};

class Minus :public Operator {
public:
	Minus() :Operator("-", 2, 2) {}
	double get(double a, double b) const {
		return a - b;
	}
};

class Multiply :public Operator {
public:
	Multiply() :Operator("*", 2, 3) {}
	double get(double a, double b) const {
		return a * b;
	}
};

class Divide :public Operator {
public:
	Divide() :Operator("/", 2, 3) {}
	double get(double a, double b) const {
		if (b == 0)
			throw "Divisor 0, didn't you graduate from primary school?";
		return a / b;
	}
};

class Mod :public Operator {
public:
	Mod() :Operator("%", 2, 3) {}
	double get(double a, double b) const {
		return static_cast<int>(a) / static_cast<int>(b);
	}
};

class Power :public Operator {
public:
	Power() :Operator("^", 2, 4) {}
	double get(double a, double b) const {
		return pow(a, b);
	}
};

class Hash : public Operator {
public:
	Hash() :Operator("#", 1, 1) {}
	double get(double a, double b) const {
		return a;
	}
};

class Equal : public Operator {
public:
	Equal() :Operator("=", 2, 0) {}
	double get(double a, double b) const {
		return a;
	}
};

class Log : public Operator {					//默认
public:
	Log() :Operator("log", 1, 5) {}
	double get(double a, double b) const {
		if (b <= 0)
			throw "If I remember correctly, the value after the log function should be greater than 0.";
		return log10(b);
	}
};

class Ln : public Operator {					//默认
public:
	Ln() :Operator("ln", 1, 5) {}
	double get(double a, double b) const {
		if (b <= 0)
			throw "If I remember correctly, the value after the log function should be greater than 0.";
		return log(b);
	}
};

class Sin : public Operator {					//默认
public:
	Sin() :Operator("sin", 1, 5) {}
	double get(double a, double b) const {
		return sin(b);
	}
};

class Cos : public Operator {
public:
	Cos() :Operator("cos", 1, 5) {}
	double get(double a, double b) const {
		return cos(b);
	}
};

class Tan : public Operator {
public:
	Tan() :Operator("tan", 1, 5) {}
	double get(double a, double b) const {
		return tan(b);
	}
};

class dtor : public Operator {
public:
	dtor() :Operator("dtor", 1, 5) {}
	double get(double a, double b) const {
		return (b / 180) * 3.14159265358979323846;
	}
};

class Sqrt : public Operator {
public:
	Sqrt() :Operator("sqrt", 1, 5) {}
	double get(double a, double b) const {
		return sqrt(b);
	}
};


#endif // !OPERATOR_H
