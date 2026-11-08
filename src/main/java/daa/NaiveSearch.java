package daa;

import java.util.ArrayList;
import java.util.List;

public final class NaiveSearch implements StringSearch {
    private long comparisons;
    public List<Integer> search(String text, String pattern) {
        comparisons = 0;
        if (pattern.isEmpty()) throw new IllegalArgumentException("Empty pattern");
        List<Integer> matches = new ArrayList<>();
        for (int i = 0; i <= text.length() - pattern.length(); i++) {
            int j = 0;
            while (j < pattern.length()) {
                comparisons++;
                if (text.charAt(i + j) != pattern.charAt(j)) break;
                j++;
            }
            if (j == pattern.length()) matches.add(i);
        }
        return matches;
    }

    public long comparisons() { return comparisons; }
}
