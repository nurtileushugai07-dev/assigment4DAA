package daa;

import java.util.Random;

public final class InputGenerator {
    public static final long SEED = 20261108L;
    private InputGenerator() { }

    public static String randomString(Random random, int length) {
        StringBuilder out = new StringBuilder(length);
        for (int i = 0; i < length; i++) out.append("ABCD".charAt(random.nextInt(4)));
        return out.toString();
    }

    public static String[] edit(String type, int n) {
        if (type.equals("worst")) return new String[]{"A".repeat(n), "B".repeat(n)};
        Random random = new Random(SEED + n);
        return new String[]{randomString(random, n), randomString(random, n)};
    }

    public static String[] search(String type, int n) {
        int m = n / 32;
        if (type.equals("worst")) return new String[]{"A".repeat(n), "A".repeat(m - 1) + "B"};
        Random random = new Random(SEED + 100000L + n);
        return new String[]{randomString(random, n), randomString(random, m)};
    }
}
