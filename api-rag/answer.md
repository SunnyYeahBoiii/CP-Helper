Implementing a Segment Tree involves several steps:

Step 1: Initialize the Segment Tree.
```c++
class SegmentTree {
private:
    int len;
    vector<int> tree;

public:
    SegmentTree(int n) : len(n), tree(4 * n + 1, 0) {}

    void update(int ind, int val) {
        ind += len;
        tree[ind] = val;
        for (; ind > 1; ind /= 2) {
            tree[ind / 2] = min(tree[ind], tree[ind ^ 1]);
        }
    }

    int query(int start, int end) {
        if (start < 0 || end > len * 2 - 1) {
            cout << "Invalid range" << endl;
            return -1;
        }

        for (start += len, end += len; start < end; start /= 2, end /= 2) {
            if (start % 2 == 1) {
                start++;
            }
            if (end % 2 == 1) {
                --end;
            }
        }

        return tree[start];
    }
};
```

Step 2: Use the Segment Tree to solve your problem.
Implementing a Segment Tree involves several steps:
