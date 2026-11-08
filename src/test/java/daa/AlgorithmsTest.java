package daa;

import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Random;
import static org.junit.jupiter.api.Assertions.*;

class AlgorithmsTest {
    private EditDistance[] edits() {
        return new EditDistance[]{new RecursiveEditDistance(), new TableEditDistance(), new TwoRowEditDistance()};
    }
    private StringSearch[] searches() { return new StringSearch[]{new NaiveSearch(), new KmpSearch()}; }

    @Test void referenceEditDistancesAndEmptyStrings() {
        for (EditDistance algorithm : edits()) {
            assertEquals(3, algorithm.distance("kitten", "sitting"));
            assertEquals(2, algorithm.distance("flaw", "lawn"));
            assertEquals(5, algorithm.distance("intention", "execution"));
            assertEquals(3, algorithm.distance("", "abc"));
            assertEquals(3, algorithm.distance("abc", ""));
            assertEquals(0, algorithm.distance("", ""));
            assertEquals(0, algorithm.distance("abc", "abc"));
        }
    }

    @Test void oneHundredRandomEditPairsAgree() {
        Random random = new Random(20261108L);
        EditDistance[] algorithms = edits();
        for (int i = 0; i < 100; i++) {
            String a = InputGenerator.randomString(random, random.nextInt(7));
            String b = InputGenerator.randomString(random, random.nextInt(7));
            int expected = algorithms[0].distance(a, b);
            for (EditDistance algorithm : algorithms) assertEquals(expected, algorithm.distance(a, b), a + " / " + b);
        }
    }

    @Test void referenceLpsArrays() {
        KmpSearch kmp = new KmpSearch();
        assertArrayEquals(new int[]{0,1,2,0,1,2,3,3}, kmp.lps("AAACAAAA"));
        assertArrayEquals(new int[]{0,0,1,2,0,1,2,3,4}, kmp.lps("ABABCABAB"));
        assertArrayEquals(new int[0], kmp.lps(""));
        assertArrayEquals(new int[]{0}, kmp.lps("A"));
    }

    @Test void referenceMatchesAndOverlaps() {
        for (StringSearch algorithm : searches()) {
            assertEquals(List.of(10), algorithm.search("ABABDABACDABABCABAB", "ABABCABAB"));
            assertEquals(List.of(0,1,2,3), algorithm.search("AAAAA", "AA"));
            assertEquals(List.of(0,2,4), algorithm.search("ABABABA", "ABA"));
            assertEquals(List.of(0,2), algorithm.search("ABA", "A"));
            assertEquals(List.of(0), algorithm.search("ABC", "ABC"));
            assertEquals(List.of(), algorithm.search("ABC", "D"));
        }
    }

    @Test void searchEdgeCases() {
        for (StringSearch algorithm : searches()) {
            assertThrows(IllegalArgumentException.class, () -> algorithm.search("abc", ""));
            assertThrows(IllegalArgumentException.class, () -> algorithm.search("", ""));
            assertEquals(List.of(), algorithm.search("a", "ab"));
            assertEquals(List.of(), algorithm.search("", "a"));
        }
    }

    @Test void oneHundredRandomSearchesAgree() {
        Random random = new Random(481516L);
        for (int i = 0; i < 100; i++) {
            String text = InputGenerator.randomString(random, random.nextInt(81));
            // Half of eligible cases deliberately contain a match; others may have none.
            String pattern = i % 2 == 0 && !text.isEmpty()
                    ? text.substring(0, 1 + random.nextInt(Math.min(8, text.length())))
                    : InputGenerator.randomString(random, 1 + random.nextInt(12));
            assertEquals(new NaiveSearch().search(text, pattern), new KmpSearch().search(text, pattern));
        }
    }

    @Test void countersMeasureWorkAndReset() {
        for (EditDistance algorithm : edits()) {
            algorithm.distance("A", "B");
            assertEquals(algorithm instanceof RecursiveEditDistance ? 4 : 1, algorithm.operations());
            algorithm.distance("", "");
            assertEquals(algorithm instanceof RecursiveEditDistance ? 1 : 0, algorithm.operations());
        }
        for (StringSearch algorithm : searches()) {
            algorithm.search("AAA", "AB");
            assertEquals(algorithm instanceof KmpSearch ? 6 : 4, algorithm.comparisons());
            algorithm.search("A", "AA");
            assertEquals(0, algorithm.comparisons());
        }
    }
}
