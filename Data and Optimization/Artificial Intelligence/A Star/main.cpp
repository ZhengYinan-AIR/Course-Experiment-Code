#pragma warning(disable:4996)
#include "puzzle.h"
#include "DFS.h"
#include "BFS.h"
#include "AStar.h"
#include <windows.h> 

using namespace std;

//计算逆序数
int getInvCount(vector<int> arr) {
    int inv_count = 0;
    for (int i = 0; i < 9 - 1; i++)
        for (int j = i + 1; j < 9; j++)
            // Value 0 is used for empty space 
            if (arr[j] && arr[i] && arr[i] > arr[j])
                inv_count++;
    return inv_count;
}

//根据逆序数判断是否有解
bool isSolvable(vector<int> src) {
    // Count inversions in given 8 puzzle 
    int invSrc = getInvCount(src);
    // return true if inversion count is even. 
    return invSrc % 2 == 0;
}

//洗牌算法，获取随机数组
vector<int> randomSource() {
    srand((unsigned)time(NULL));
    vector<int> res{ 1, 2, 3, 4, 5, 6, 7, 8, 0 };
    for (int i = 0; i < 9; ++i) {
        int j = rand() % (9-i) + i;
        swap(res[i], res[j]);
    }
    return res;
}

//八数码初始状态
vector<int> source;

//Astar线程
DWORD WINAPI f_astar(LPVOID lpParamter) {
    puzzle* astar = new AStar(source);
    astar->start();
    return 0L;
}

//DFS线程
DWORD WINAPI f_dfs(LPVOID lpParamter) {
    puzzle* dfs = new DFS(source);
    dfs->start();
    return 0L;
}

//BFS线程
DWORD WINAPI f_bfs(LPVOID lpParamter) {
    puzzle* bfs = new BFS(source);
    bfs->start();
    return 0L;
}

int main() {
    initgraph(1200, 400);	// 创建绘图窗口
    
    //获取有解的八数码
    do {
        source = randomSource();
    } while (!isSolvable(source));

    //启动三个线程
    HANDLE t_astar = CreateThread(NULL, 0, f_astar, NULL, 0, NULL);
    HANDLE t_dfs = CreateThread(NULL, 0, f_dfs, NULL, 0, NULL);
    HANDLE t_bfs = CreateThread(NULL, 0, f_bfs, NULL, 0, NULL);
    
    if (t_astar) CloseHandle(t_astar);
    if (t_dfs) CloseHandle(t_dfs);
    if (t_bfs) CloseHandle(t_bfs);

    char ch = _getch();

	return 0;
}