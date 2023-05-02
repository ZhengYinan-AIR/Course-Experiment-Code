#ifndef E_PUZZLE
#define E_PUZZLE

#include <vector>
#include <string>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <iostream>
#include <algorithm>
#include <graphics.h>
#include <conio.h>
#include <mutex>


std::mutex mtx;

// 将 ANSI char* 转为 unicode
LPCTSTR cstr2L(char* str) {
	int num = MultiByteToWideChar(0, 0, str, -1, NULL, 0);
	wchar_t* wide = new wchar_t[num];
	MultiByteToWideChar(0, 0, str, -1, wide, num);
	return wide;
}

// 数组转数字
int arr2num(std::vector<int> arr) {
	int res = 0;
	for (int i = 0; i < 9; ++i) {
		res = res * 10 + arr[i];
	}
	return res;
}

// 数字转数组
std::vector<int> num2arr(int num) {
	std::vector<int> res;
	for (int i = 0; i < 9; ++i) {
		res.push_back(num % 10);
		num /= 10;
	}
	std::reverse(res.begin(), res.end());
	return res;
}

// 三个算法的公共父类
class puzzle
{
protected:
	const char* name; //算法名称
	const char* SDIGIT[9] = {" ", "1", "2", "3", "4", "5", "6", "7", "8"}; //各个数字对应的字符串
	int ANSARR[9] = { 1, 2, 3, 4, 5, 6, 7, 8, 0 }; //目标状态的数组形式
	int ANSNUM = 123456780; //目标状态的数字形式
	int dd[4] = { 1, -1, 3, -3 }; //移动0的位移量
	int WIDTH = 1200; //窗口宽度
	int HEIGHT = 400; //窗口高度
	int offsetX = 50; //九宫格X偏移
	int offsetY = 50; //九宫格Y偏移

	std::vector<int> state; //初始状态
	std::unordered_map<int, int> parent; //每个状态的父亲
	std::unordered_set<int> visited; //记录已访问过的状态
	int count = 1; //搜索次数
	int pathCount = 0; //解法步数
	bool solved = false; //已解决
	RECT rect; //当前算法的子窗口位置
	RECT titleRect; //当前算法的标题位置
	RECT bottomRect; //当前算法的下部说明文字位置
	RECT digitRect[9]; //当前算法九宫格的位置
	UINT wordPos = DT_CENTER | DT_VCENTER | DT_SINGLELINE; //设定绘制文字规则（水平垂直居中，单行显示）

	//是否有解
	bool isSolve(std::vector<int> arr) {
		for (int i = 0; i < 9; ++i) {
			if (arr[i] != ANSARR[i]) return false;
		}
		return true;
	}

	bool isSolve(int num) {
		return isSolve(num2arr(num));
	}

	//输出状态
	void outState(std::vector<int> arr) {
		for (int i = 0; i < 9; ++i) {
			if (i % 3 == 0) std::cout << std::endl;
			std::cout << arr[i] << ' ';
		}
		std::cout << std::endl << "-----" << std::endl;
	}

	void outState(int num) {
		outState(num2arr(num));
	}

	//获取0的下标
	int zeroIndex(std::vector<int> arr) {
		for (int i = 0; i < 9; ++i) {
			if (arr[i] == 0) return i;
		}
		return -1;
	}

	int zeroIndex(int num) {
		return zeroIndex(num2arr(num));
	}

	//绘制九宫格
	void draw(std::vector<int> arr, bool showCount) {
		for (int i = 0; i < 9; ++i) {
			drawtext((LPCTSTR)SDIGIT[arr[i]], &digitRect[i], wordPos);
		}

		if (showCount) {
			char buffer[20];
			sprintf(buffer, "搜索次数：%d", count);
			drawtext(cstr2L(buffer), &titleRect, wordPos);
		}
	}

	//搜索前的动作
	void beforeSearch() {
		drawtext(_T("搜索中"), &titleRect, wordPos);
		drawtext(cstr2L((char*)name), &bottomRect, wordPos);
	}

	//完成搜索后的动作
	void finishSearch() {
		if (pathCount == 0) pathCount = getPath().size();
		char buffer[50];
		sprintf(buffer, "%s,搜%d次,走%d步", name, count, pathCount);
		drawtext(_T("               "), &bottomRect, wordPos);
		settextstyle(30, 0, _T("Consolas"));
		drawtext(cstr2L(buffer), &bottomRect, wordPos);
		settextstyle(40, 0, _T("Consolas"));
		if (solved) {
			drawtext(_T("搜索完毕,找到解法"), &titleRect, wordPos);
		}
		else {
			drawtext(_T("搜索完毕,未找到解法"), &titleRect, wordPos);
		}
	}

	//演示搜索结果
	void showPath() {
		drawtext(_T("    开始演示解法    "), &titleRect, wordPos);
		std::vector< std::vector<int> > paths = getPath();
		pathCount = paths.size();
		for (std::vector<int> path : paths) {
			draw(path, false);
			Sleep(1000);
		}
		drawtext(_T("    演示结束    "), &titleRect, wordPos);
	}
public:
	//构造函数，设置初始状态、子窗口位置、算法名称
	puzzle(std::vector<int> _state, int id, const char* _name) {
		state = _state;
		name = _name;
		int w = WIDTH / 3, h = HEIGHT;
		rect = { w * id, 0, w * (id+1), h };

		titleRect = { w * id, 0, w * (id + 1), offsetY };
		bottomRect = { w * id, h - offsetX, w * (id + 1), h };

		int rw = (w - offsetX*2) / 3, rh = (h - offsetY*2) / 3;

		setfillcolor(BLACK);
		settextstyle(40, 0, _T("Consolas"));

		for (int i = 0; i < 3; ++i) {
			for (int j = 0; j < 3; ++j) {
				int n = i + j * 3;
				digitRect[n] = { 
					rect.left + offsetX + rw * i, 
					rect.top + offsetY + rh * j,
					rect.left + offsetX + rw * i + rw,
					rect.top + offsetY + rh * j + rh
				};
				fillrectangle(digitRect[n].left, digitRect[n].top, digitRect[n].right, digitRect[n].bottom);
			}
		}
	}

	//入口函数
	void start() {
		beforeSearch();
		run();
		finishSearch();
		Sleep(2000);
		if(solved) showPath();
	}

	//运行的函数，留给各个算法子类实现
	virtual void run() {
	}

	//获取搜索路径结果
	std::vector< std::vector<int> > getPath() {
		std::vector< std::vector<int>> res;
		if (!solved) return res;
		int now = 123456780;
		res.push_back(num2arr(now));
		while (now = parent[now]) {
			res.push_back(num2arr(now));
		}
		std::reverse(res.begin(), res.end());
		return res;
	}

	//获取搜索次数（状态数）
	int getStateCount() {
		return count;
	}
};

#endif

