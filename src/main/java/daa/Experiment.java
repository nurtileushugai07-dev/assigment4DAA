package daa;

import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

public final class Experiment {
    private static final int RUNS = 3;
    private static volatile int sink;

    public static void main(String[] args) throws Exception {
        Path output = Path.of(args.length == 0 ? "results/results.csv" : args[0]);
        if (output.getParent() != null) Files.createDirectories(output.getParent());
        try (PrintWriter csv = new PrintWriter(Files.newBufferedWriter(output))) {
            csv.println("family,algorithm,input,n,m,run,time_ms,operations,counter,result,seed");
            EditDistance[] edits = {new RecursiveEditDistance(), new TableEditDistance(), new TwoRowEditDistance()};
            String[] editNames = {"recursive", "table", "two_rows"};
            for (int k = 0; k < edits.length; k++) {
                int[] sizes = k == 0 ? new int[]{3, 6, 9, 12} : new int[]{128, 256, 512, 1024};
                for (String type : new String[]{"random", "worst"}) {
                    for (int n : sizes) {
                        String[] pair = InputGenerator.edit(type, n);
                        int expected = new TwoRowEditDistance().distance(pair[0], pair[1]);
                        EditDistance algorithm = edits[k];
                        sink = algorithm.distance(pair[0], pair[1]); // warm-up
                        double[] times = new double[RUNS];
                        for (int run = 1; run <= RUNS; run++) {
                            long start = System.nanoTime();
                            int answer = algorithm.distance(pair[0], pair[1]);
                            times[run - 1] = (System.nanoTime() - start) / 1_000_000.0;
                            sink = answer;
                            if (answer != expected) throw new AssertionError("Edit result mismatch");
                            row(csv, "edit", editNames[k], type, n, n, run, times[run - 1],
                                    algorithm.operations(), k == 0 ? "calls" : "cells", answer);
                        }
                        show(editNames[k], type, n, times, algorithm.operations());
                    }
                }
            }
            StringSearch[] searches = {new NaiveSearch(), new KmpSearch()};
            String[] searchNames = {"naive", "kmp"};
            for (int k = 0; k < searches.length; k++) {
                for (String type : new String[]{"random", "worst"}) {
                    for (int n : new int[]{4096, 8192, 16384, 32768}) {
                        String[] pair = InputGenerator.search(type, n);
                        List<Integer> expected = new KmpSearch().search(pair[0], pair[1]);
                        StringSearch algorithm = searches[k];
                        sink = algorithm.search(pair[0], pair[1]).size();
                        double[] times = new double[RUNS];
                        for (int run = 1; run <= RUNS; run++) {
                            long start = System.nanoTime();
                            List<Integer> matches = algorithm.search(pair[0], pair[1]);
                            times[run - 1] = (System.nanoTime() - start) / 1_000_000.0;
                            sink = matches.size();
                            if (!matches.equals(expected)) throw new AssertionError("Search result mismatch");
                            row(csv, "search", searchNames[k], type, n, pair[1].length(), run,
                                    times[run - 1], algorithm.comparisons(), "comparisons", matches.size());
                        }
                        show(searchNames[k], type, n, times, algorithm.comparisons());
                    }
                }
            }
        }
        System.out.println("Saved " + output + " (120 measured runs).");
    }

    private static void row(PrintWriter out, String family, String algorithm, String type, int n, int m,
                            int run, double ms, long operations, String counter, int result) {
        out.printf(Locale.ROOT, "%s,%s,%s,%d,%d,%d,%.6f,%d,%s,%d,%d%n",
                family, algorithm, type, n, m, run, ms, operations, counter, result, InputGenerator.SEED);
    }

    private static void show(String algorithm, String type, int n, double[] times, long operations) {
        Arrays.sort(times);
        System.out.printf(Locale.ROOT, "%s %-6s n=%d median=%.6f ms operations=%d%n",
                algorithm, type, n, times[RUNS / 2], operations);
    }
}
