import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.PriorityQueue;
import java.util.StringTokenizer;
import java.util.TreeMap;

public class Main {
    FastScanner in;
    PrintWriter out;

    private void solve() throws IOException {
        int n = in.nextInt();

        String[] q = new String[n];
        int qs = 0, wait = 0;
        TreeMap<String, Integer> map = new TreeMap<>();
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        for (int i = 0; i < n; i++) {
            String s = in.next();
            if (s.equals("next")) {
                if (pq.isEmpty())
                    wait++;
                else
                    out.println(q[pq.remove()]);
            } else {
                if (map.containsKey(s)) {
                    out.println("2nd " + s);
                    pq.add(map.get(s));
                    map.remove(s);
                    if (wait > 0) {
                        out.println(q[pq.remove()]);
                        wait--;
                    }
                } else {
                    out.println("1st " + s);
                    map.put(s, qs);
                    q[qs++] = s;
                }
            }
        }
    }

    class FastScanner {
        StringTokenizer st;
        BufferedReader br;

        FastScanner(InputStream s) {
            br = new BufferedReader(new InputStreamReader(s));
        }

        String next() throws IOException {
            while (st == null || !st.hasMoreTokens())
                st = new StringTokenizer(br.readLine());
            return st.nextToken();
        }

        boolean hasNext() throws IOException {
            return br.ready() || (st != null && st.hasMoreTokens());
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }

        long nextLong() throws IOException {
            return Long.parseLong(next());
        }

        double nextDouble() throws IOException {
            return Double.parseDouble(next());
        }

        String nextLine() throws IOException {
            return br.readLine();
        }

        boolean hasNextLine() throws IOException {
            return br.ready();
        }
    }

    private void run() throws IOException {
        in = new FastScanner(System.in);
        out = new PrintWriter(System.out);

        solve();

        out.flush();
        out.close();
    }

    public static void main(String[] args) throws IOException {
        new Main().run();
    }
}