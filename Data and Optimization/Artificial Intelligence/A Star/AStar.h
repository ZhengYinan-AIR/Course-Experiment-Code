#ifndef E_ASTAR
#define E_ASTAR

#include "puzzle.h"

//每个点对应的曼哈顿距离
int manhattan[10][10] = {
    {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1},
    {-1, 0, 1, 2, 1, 2, 3, 2, 3, 4},
    {-1, 1, 0, 1, 2, 1, 2, 3, 2, 3},
    {-1, 2, 1, 0, 3, 2, 1, 4, 3, 2},
    {-1, 1, 2, 3, 0, 1, 2, 1, 2, 3},
    {-1, 2, 1, 2, 1, 0, 1, 2, 1, 2},
    {-1, 3, 2, 1, 2, 1, 0, 3, 2, 1},
    {-1, 2, 3, 4, 1, 2, 3, 0, 1, 2},
    {-1, 3, 2, 3, 2, 1, 2, 1, 0, 1},
    {-1, 4, 3, 2, 3, 2, 1, 2, 1, 0}
};

class AStar : public puzzle
{
private:
    static int AScore(std::vector<int> arr, int s) {
        int score = s;
        for (int i = 0; i < 9; ++i) {
            score += manhattan[i + 1][arr[i]];
        }
        return score;
    }

    //存储九宫格状态和步数，根据估价函数重载小于运算符，用于优先队列自动获取最优解。
    struct Node {
        int num, step;
        Node(int n, int s): num(n), step(s) {}
        bool operator<(const Node b) const {
            int as = AScore(num2arr(num), step);    //step为深度
            int bs = AScore(num2arr(b.num), b.step);
            return as > bs;
        }
    };

    bool runAStar(int stateNum) {
        std::priority_queue<Node, std::vector<Node>> q;
        Node root = Node(stateNum, 0);
        q.push(root);
        while (q.size() && !solved) {
            count++;
            Node now = q.top(); //取优先队列堆顶元素，也就是估价函数的最优解
            q.pop();

            if (visited.count(now.num)) continue; //去除已访问过的情况
            visited.insert(now.num); //记录已访问状态，不同表对应的stateNum的数不同
            std::vector<int> arr = num2arr(now.num);

            //draw(arr, true);

            //当前是正确解答，则返回结果
            if (now.num == ANSNUM) {
                solved = true;
                return true;
            }
            
            int idx = zeroIndex(arr);
            for (int i = 0; i < 4; ++i) {
                if (idx % 3 == 0 && i == 1) continue;
                if (idx % 3 == 2 && i == 0) continue;
                int next_idx = idx + dd[i];
                if (next_idx >= 0 && next_idx < 9) {
                    std::swap(arr[idx], arr[next_idx]);
                    int tmp = arr2num(arr);
                    if (!visited.count(tmp)) {
                        parent[tmp] = now.num;
                        q.push(Node(tmp, now.step+1));
                    }

                    std::swap(arr[idx], arr[next_idx]);
                }
            }
        }
        return false;
    }
public:
    AStar(std::vector<int> _state) : puzzle(_state, 0, "AStar") {}
    void run() {
        runAStar(arr2num(state));
    }
};

#endif

