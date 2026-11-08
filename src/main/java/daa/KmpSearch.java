package daa;

import java.util.ArrayList;
import java.util.List;

public final class KmpSearch implements StringSearch {
    private long comparisons;

    // LPS[i]: longest proper prefix of p[0..i] that is also a suffix.
    public int[] lps(String p) {
        comparisons = 0;
        return buildLps(p);
    }

    private int[] buildLps(String p) {
        int[] lps = new int[p.length()];
        int i = 1, length = 0;
        while (i < p.length()) {
            comparisons++;
            if (p.charAt(i) == p.charAt(length)) lps[i++] = ++length;
            else if (length > 0) length = lps[length - 1];
            else lps[i++] = 0;
        }
        return lps;
    }

    public List<Integer> search(String text, String pattern) {
        comparisons = 0;
        if (pattern.isEmpty()) throw new IllegalArgumentException("Empty pattern");
        List<Integer> matches = new ArrayList<>();
        if (pattern.length() > text.length()) return matches;
        int[] lps = buildLps(pattern); // preprocessing comparisons are included
        int i = 0, j = 0;
        while (i < text.length()) {
            comparisons++;
            if (text.charAt(i) == pattern.charAt(j)) {
                i++; j++;
                if (j == pattern.length()) {
                    matches.add(i - j);
                    j = lps[j - 1]; // permits overlapping matches
                }
            } else if (j > 0) j = lps[j - 1];
            else i++;
        }
        return matches;
    }

    public long comparisons() { return comparisons; }
}
