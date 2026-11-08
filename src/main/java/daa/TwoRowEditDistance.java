package daa;

public final class TwoRowEditDistance implements EditDistance {
    private long cells;
    // State: prev[j]=D(i-1,j), curr[j]=D(i,j), distances between prefixes.
    // Transition: equal -> prev[j-1]; otherwise 1+min(prev[j],curr[j-1],prev[j-1]).
    // Base: prev[j]=j for row 0; curr[0]=i for each new row.
    public int distance(String a, String b) {
        cells = 0;
        int m = b.length();
        int[] prev = new int[m + 1], curr = new int[m + 1];
        for (int j = 0; j <= m; j++) prev[j] = j;
        for (int i = 1; i <= a.length(); i++) {
            curr[0] = i;
            for (int j = 1; j <= m; j++) {
                cells++;
                curr[j] = a.charAt(i - 1) == b.charAt(j - 1) ? prev[j - 1]
                        : 1 + Math.min(prev[j - 1], Math.min(prev[j], curr[j - 1]));
            }
            int[] temp = prev; prev = curr; curr = temp;
        }
        return prev[m];
    }

    public long operations() { return cells; }
}
