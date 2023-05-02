#ifndef E_DFS
#define E_DFS

#include "puzzle.h"

class DFS : public puzzle
{
private:
	int MAX = 50; //最大递归深度

    bool dfs(int stateNum, int idx, int d_step) {
        std::vector<int> stateArr = num2arr(stateNum);
        //draw(stateArr, true);

        if (d_step >= MAX || visited.count(stateNum)) return false;
        visited.insert(stateNum);
        if (stateNum == ANSNUM) {
            solved = true;
            return true;
        }
        count++;

        for (int i = 0; i < 4; ++i) {
            if (idx % 3 == 0 && i == 1) continue;
            if (idx % 3 == 2 && i == 0) continue;
            int next_idx = idx + dd[i];
            if (next_idx >= 0 && next_idx < 9) {
                std::swap(stateArr[idx], stateArr[next_idx]);
                int tmp = arr2num(stateArr);
                if(!visited.count(tmp))parent[tmp] = stateNum;
                if (dfs(tmp, next_idx, d_step+1)) return true;
                std::swap(stateArr[idx], stateArr[next_idx]);
            }
        }
        return false;
    }
public:
    DFS(std::vector<int> _state): puzzle(_state, 2, "DFS") {}
	void run() {
        dfs(arr2num(state), zeroIndex(state), 0);
	}
};

#endif

