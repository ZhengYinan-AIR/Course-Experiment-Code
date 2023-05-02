#ifndef OPERATORFACTORY_H
#define OPERATORFACTORY_H

#include<string>
#include<map>
#include<functional>
#include<memory>
#include"Operator.h"

// ע��Object�ĺ�����
#define REGISTRAROPR(T, Key)  Factory::RegisterClass_opr<T> reg_##T(Key);
#define REGISTRARFUN(T, Key)  Factory::RegisterClass_fun<T> reg_##T(Key);

using namespace std;

class Factory {
public:
	template<typename T>
	struct RegisterClass_opr {
		RegisterClass_opr(string opr) {
			Factory::ms_operator.emplace(opr, [] {return make_unique<T>(); });
		}
	};
	template<typename T>
	struct RegisterClass_fun {
		RegisterClass_fun(string fun) {
			Factory::ms_function.emplace(fun, [] {return make_unique<T>(); });
		}
	};

	static unique_ptr<Operator> create_opr(string opr) {
		auto it = ms_operator.find(opr);
		if (it != ms_operator.end())
			return it->second();						
		else
			throw "Well, our calculator doesn't seem to have this operator!";
	}
	static unique_ptr<Operator> create_fun(string fun) {
		auto it = ms_function.find(fun);
		if (it != ms_function.end())
			return it->second();
		else
			throw "Well, our calculator doesn't seem to have this function!";
	}
	//private:
	static map<string, function<unique_ptr<Operator>()>> ms_operator; // �洢��ע�������������Ӧ��������ָ���map
	static map<string, function<unique_ptr<Operator>()>> ms_function; // �洢��ע�ắ��������Ӧ��������ָ���map
};

#endif


