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
        (void)(a);
        return b;
    }
};

class Rbra :public Operator {
public:
    Rbra() :Operator(")", 1, 0) {}
    double get(double a, double b) const {
        (void)(b);
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
            throw "/ invalid input";
        return a / b;
    }
};

class Mod :public Operator {
public:
    Mod() :Operator("%", 2, 3) {}
    double get(double a, double b) const {
        if(static_cast<int>(b)==0)
            throw "% invalid input";
        int i = static_cast<int>(a) / static_cast<int>(b);
        return static_cast<int>(a)-i*static_cast<int>(b);
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
        (void)(b);
        return a;
    }
};

class Equal : public Operator {
public:
    Equal() :Operator("=", 2, 0) {}
    double get(double a, double b) const {
        (void)(b);
        return a;
    }
};

class Fac : public Operator {					//默认
public:
    Fac() :Operator("!", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        int item = int(b);
        int result = 1;
        for(int i =1;i<=item;++i){
            result *= i;
        }
       return result;
    }
};

class Log : public Operator {					//默认
public:
    Log() :Operator("log", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if (b <= 0)
            throw "log() invalid input";
        return log10(b);
    }
};

class Ln : public Operator {					//默认
public:
    Ln() :Operator("ln", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if (b <= 0)
            throw "ln() invalid input";
        return log(b);
    }
};

class Sin : public Operator {					//默认
public:
    Sin() :Operator("sin", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        return sin(b);
    }
};

class Cos : public Operator {
public:
    Cos() :Operator("cos", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        return cos(b);
    }
};

class Tan : public Operator {
public:
    Tan() :Operator("tan", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if(b == 3.14159265358979323846/2)
            throw "tan() invalid input";
        return tan(b);
    }
};

class aSin : public Operator {					//默认
public:
    aSin() :Operator("asin", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if(b>1||b<-1)
            throw "asin() invalid input";
        return asin(b);
    }
};

class aCos : public Operator {
public:
    aCos() :Operator("acos", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if(b>1||b<-1)
            throw "acos() invalid input";
        return acos(b);
    }
};

class aTan : public Operator {
public:
    aTan() :Operator("atan", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        return atan(b);
    }
};

class dtor : public Operator {
public:
    dtor() :Operator("dtor", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        return (b / 180) * 3.14159265358979323846;
    }
};

class rtod : public Operator {
public:
    rtod() :Operator("rtod", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        return b/3.14159265358979323846*180;
    }
};

class Sqrt : public Operator {
public:
    Sqrt() :Operator("sqrt", 1, 5) {}
    double get(double a, double b) const {
        (void)(a);
        if(b<0)
            throw "sqrt() invalid input";
        return sqrt(b);
    }
};

#endif // OPERATOR_H
