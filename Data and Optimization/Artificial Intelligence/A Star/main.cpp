#pragma warning(disable:4996)
#include "puzzle.h"
#include "DFS.h"
#include "BFS.h"
#include "AStar.h"
#include <windows.h> 

using namespace std;

//����������
int getInvCount(vector<int> arr) {
    int inv_count = 0;
    for (int i = 0; i < 9 - 1; i++)
        for (int j = i + 1; j < 9; j++)
            // Value 0 is used for empty space 
            if (arr[j] && arr[i] && arr[i] > arr[j])
                inv_count++;
    return inv_count;
}

//�����������ж��Ƿ��н�
bool isSolvable(vector<int> src) {
    // Count inversions in given 8 puzzle 
    int invSrc = getInvCount(src);
    // return true if inversion count is even. 
    return invSrc % 2 == 0;
}

//ϴ���㷨����ȡ�������
vector<int> randomSource() {
    srand((unsigned)time(NULL));
    vector<int> res{ 1, 2, 3, 4, 5, 6, 7, 8, 0 };
    for (int i = 0; i < 9; ++i) {
        int j = rand() % (9-i) + i;
        swap(res[i], res[j]);
    }
    return res;
}

//�������ʼ״̬
vector<int> source;

//Astar�߳�
DWORD WINAPI f_astar(LPVOID lpParamter) {
    puzzle* astar = new AStar(source);
    astar->start();
    return 0L;
}

//DFS�߳�
DWORD WINAPI f_dfs(LPVOID lpParamter) {
    puzzle* dfs = new DFS(source);
    dfs->start();
    return 0L;
}

//BFS�߳�
DWORD WINAPI f_bfs(LPVOID lpParamter) {
    puzzle* bfs = new BFS(source);
    bfs->start();
    return 0L;
}

int main() {
    initgraph(1200, 400);	// ������ͼ����
    
    //��ȡ�н�İ�����
    do {
        source = randomSource();
    } while (!isSolvable(source));

    //���������߳�
    HANDLE t_astar = CreateThread(NULL, 0, f_astar, NULL, 0, NULL);
    HANDLE t_dfs = CreateThread(NULL, 0, f_dfs, NULL, 0, NULL);
    HANDLE t_bfs = CreateThread(NULL, 0, f_bfs, NULL, 0, NULL);
    
    if (t_astar) CloseHandle(t_astar);
    if (t_dfs) CloseHandle(t_dfs);
    if (t_bfs) CloseHandle(t_bfs);

    char ch = _getch();

	return 0;
}