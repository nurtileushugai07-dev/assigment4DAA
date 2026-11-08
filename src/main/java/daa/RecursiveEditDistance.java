package daa;

public final class RecursiveEditDistance implements EditDistance {
    private long calls;
    // State: D(i,j) is the distance between prefixes a[0..i) and b[0..j).
    // Transition: equal last characters -> D(i-1,j-1); otherwise 1+min(delete,insert,replace).
    // Base: D(0,j)=j and D(i,0)=i. No memoization: repeated states are recomputed.
    public int distance(String a, String b) {
        calls = 0;
        return solve(a, b, a.length(), b.length());
    }

    private int solve(String a, String b, int i, int j) {
        calls++;
        if (i == 0) return j;
        if (j == 0) return i;
        if (a.charAt(i - 1) == b.charAt(j - 1)) return solve(a, b, i - 1, j - 1);
        return 1 + Math.min(solve(a, b, i - 1, j),
                Math.min(solve(a, b, i, j - 1), solve(a, b, i - 1, j - 1)));
    }

    public long operations() { return calls; }
}
