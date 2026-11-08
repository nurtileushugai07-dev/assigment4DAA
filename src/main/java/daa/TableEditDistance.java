package daa;

public final class TableEditDistance implements EditDistance {
    private long cells;
    // State: dp[i][j] is the edit distance of the first i and j characters.
    // Transition: equal -> dp[i-1][j-1]; otherwise 1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]).
    // Base: dp[i][0]=i and dp[0][j]=j.
    public int distance(String a, String b) {
        cells = 0;
        int n = a.length(), m = b.length();
        int[][] dp = new int[n + 1][m + 1];
        for (int i = 0; i <= n; i++) dp[i][0] = i;
        for (int j = 0; j <= m; j++) dp[0][j] = j;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                cells++;
                dp[i][j] = a.charAt(i - 1) == b.charAt(j - 1) ? dp[i - 1][j - 1]
                        : 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));
            }
        }
        return dp[n][m];
    }

    public long operations() { return cells; }
}
