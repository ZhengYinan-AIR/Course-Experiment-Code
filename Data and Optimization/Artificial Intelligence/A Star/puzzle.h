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

// �� ANSI char* תΪ unicode
LPCTSTR cstr2L(char* str) {
	int num = MultiByteToWideChar(0, 0, str, -1, NULL, 0);
	wchar_t* wide = new wchar_t[num];
	MultiByteToWideChar(0, 0, str, -1, wide, num);
	return wide;
}

// ����ת����
int arr2num(std::vector<int> arr) {
	int res = 0;
	for (int i = 0; i < 9; ++i) {
		res = res * 10 + arr[i];
	}
	return res;
}

// ����ת����
std::vector<int> num2arr(int num) {
	std::vector<int> res;
	for (int i = 0; i < 9; ++i) {
		res.push_back(num % 10);
		num /= 10;
	}
	std::reverse(res.begin(), res.end());
	return res;
}

// �����㷨�Ĺ�������
class puzzle
{
protected:
	const char* name; //�㷨����
	const char* SDIGIT[9] = {" ", "1", "2", "3", "4", "5", "6", "7", "8"}; //�������ֶ�Ӧ���ַ���
	int ANSARR[9] = { 1, 2, 3, 4, 5, 6, 7, 8, 0 }; //Ŀ��״̬��������ʽ
	int ANSNUM = 123456780; //Ŀ��״̬��������ʽ
	int dd[4] = { 1, -1, 3, -3 }; //�ƶ�0��λ����
	int WIDTH = 1200; //���ڿ��
	int HEIGHT = 400; //���ڸ߶�
	int offsetX = 50; //�Ź���Xƫ��
	int offsetY = 50; //�Ź���Yƫ��

	std::vector<int> state; //��ʼ״̬
	std::unordered_map<int, int> parent; //ÿ��״̬�ĸ���
	std::unordered_set<int> visited; //��¼�ѷ��ʹ���״̬
	int count = 1; //��������
	int pathCount = 0; //�ⷨ����
	bool solved = false; //�ѽ��
	RECT rect; //��ǰ�㷨���Ӵ���λ��
	RECT titleRect; //��ǰ�㷨�ı���λ��
	RECT bottomRect; //��ǰ�㷨���²�˵������λ��
	RECT digitRect[9]; //��ǰ�㷨�Ź����λ��
	UINT wordPos = DT_CENTER | DT_VCENTER | DT_SINGLELINE; //�趨�������ֹ���ˮƽ��ֱ���У�������ʾ��

	//�Ƿ��н�
	bool isSolve(std::vector<int> arr) {
		for (int i = 0; i < 9; ++i) {
			if (arr[i] != ANSARR[i]) return false;
		}
		return true;
	}

	bool isSolve(int num) {
		return isSolve(num2arr(num));
	}

	//���״̬
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

	//��ȡ0���±�
	int zeroIndex(std::vector<int> arr) {
		for (int i = 0; i < 9; ++i) {
			if (arr[i] == 0) return i;
		}
		return -1;
	}

	int zeroIndex(int num) {
		return zeroIndex(num2arr(num));
	}

	//���ƾŹ���
	void draw(std::vector<int> arr, bool showCount) {
		for (int i = 0; i < 9; ++i) {
			drawtext((LPCTSTR)SDIGIT[arr[i]], &digitRect[i], wordPos);
		}

		if (showCount) {
			char buffer[20];
			sprintf(buffer, "����������%d", count);
			drawtext(cstr2L(buffer), &titleRect, wordPos);
		}
	}

	//����ǰ�Ķ���
	void beforeSearch() {
		drawtext(_T("������"), &titleRect, wordPos);
		drawtext(cstr2L((char*)name), &bottomRect, wordPos);
	}

	//���������Ķ���
	void finishSearch() {
		if (pathCount == 0) pathCount = getPath().size();
		char buffer[50];
		sprintf(buffer, "%s,��%d��,��%d��", name, count, pathCount);
		drawtext(_T("               "), &bottomRect, wordPos);
		settextstyle(30, 0, _T("Consolas"));
		drawtext(cstr2L(buffer), &bottomRect, wordPos);
		settextstyle(40, 0, _T("Consolas"));
		if (solved) {
			drawtext(_T("�������,�ҵ��ⷨ"), &titleRect, wordPos);
		}
		else {
			drawtext(_T("�������,δ�ҵ��ⷨ"), &titleRect, wordPos);
		}
	}

	//��ʾ�������
	void showPath() {
		drawtext(_T("    ��ʼ��ʾ�ⷨ    "), &titleRect, wordPos);
		std::vector< std::vector<int> > paths = getPath();
		pathCount = paths.size();
		for (std::vector<int> path : paths) {
			draw(path, false);
			Sleep(1000);
		}
		drawtext(_T("    ��ʾ����    "), &titleRect, wordPos);
	}
public:
	//���캯�������ó�ʼ״̬���Ӵ���λ�á��㷨����
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

	//��ں���
	void start() {
		beforeSearch();
		run();
		finishSearch();
		Sleep(2000);
		if(solved) showPath();
	}

	//���еĺ��������������㷨����ʵ��
	virtual void run() {
	}

	//��ȡ����·�����
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

	//��ȡ����������״̬����
	int getStateCount() {
		return count;
	}
};

#endif

