//利用链栈实现
/*
1.增加弧度数字转换
2.自动删除空格将表达式转换成小写并检查有没有异常字符
3.检查括号是否匹配
1.报错处理，比如除以0
3.负数处理
*/


/*需要做
* 1.添加错误位置
* 1.做两种编辑模式，一种matlab式，一种实时计算模式
* 1.连续输入运算符，则取最后一个
1.调整精度
5.保留上次运算结果
*/
#include <string>
#include <iostream>
#include "Calculator.h"


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
REGISTRARFUN(Log, "log");
REGISTRARFUN(Ln, "ln");
REGISTRARFUN(Sin, "sin");
REGISTRARFUN(Cos, "cos");
REGISTRARFUN(Tan, "tan");
REGISTRARFUN(dtor, "dtor");
REGISTRARFUN(Sqrt, "sqrt");
double ans ;

int main() {
	string exp;
	while (getline(cin, exp)) {
		Calculator cclt;
		if (cclt.bracheck(exp) && cclt.check(exp) && cclt.del_space(exp)) {
			try {
				ans = cclt.doIt(exp);
			}
			catch (const char* str) {
				continue;
			}
			cout << ans << endl;
		}
	}
	system("pause");
	return 0;
}

