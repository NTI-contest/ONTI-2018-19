#include "testlib.h"

std::string upper(std::string sa) {
    for (size_t i = 0; i < sa.length(); i++)
        if ('a' <= sa[i] && sa[i] <= 'z')
            sa[i] = sa[i] - 'a' + 'A';
    return sa;
}

bool is_prime(long long n) {
    for (long long k = 2LL; k * k <= n; k++)
        if (n % k == 0LL)
            return 0;
    return 1;
}

int main(int argc, char * argv[]) {
    registerTestlibCmd(argc, argv);
	
	int n = inf.readInt();
    long long m = inf.readLong();
	long long a[n];
	long long sum = 0;
    for (int i = 0; i < n; i++){
        a[i] = inf.readLong();
		sum += a[i];
	}
	
    std::string ja = upper(ans.readWord());
    std::string pa = upper(ouf.readWord());
	
    if (ja != "YES" && ja != "NO")
        quitf(_fail, "YES or NO expected in answer, but %s found", ja.c_str());
	
    if (pa != "YES" && pa != "NO")
        quitf(_pe, "YES or NO expected, but %s found", pa.c_str());
	
    if (ja != pa)
        quitf(_wa, "expected %s, found %s", ja.c_str(), pa.c_str());
    
    if (ja == "NO")
        quitf(_ok, ":)");
	
	long long sumja = sum;
	if (!ans.seekEof()) {
		int i = ans.readInt();
		if (i < 1 || i > n)
			quitf(_fail, "Invalid i (i = %d)", i);
		i--;
		if (a[i] < 2LL || !is_prime(a[i]))
			quitf(_fail, "Invalid a[%d] (a[%d] = %d)", i, i, a[i]);
		if (ans.seekEof())
			quitf(_fail, "Answer does not contain k");
		long long k = ans.readLong();
		if (k < 2LL)
			quitf(_fail, "Invalid k (k = %d)", k);
		if (!ans.seekEof())
			quitf(_fail, "Answer contains extra elements");
		sumja += (k - 1LL) * a[i];
	}
	
	if (sumja != m)
		quitf(_fail, "Jury sum not equal to m");
	
	long long sumpa = sum;
	if (!ouf.seekEof()) {
		int i = ouf.readInt();
		if (i < 1 || i > n)
			quitf(_pe, "Invalid i (i = %d)", i);
		i--;
		if (a[i] < 2LL || !is_prime(a[i]))
			quitf(_wa, "Invalid a[%d] (a[%d] = %d)", i, i, a[i]);
		if (ouf.seekEof())
			quitf(_pe, "Output does not contain k");
		long long k = ouf.readLong();
		if (k < 2LL)
			quitf(_wa, "Invalid k (k = %d)", k);
		if (!ouf.seekEof())
			quitf(_pe, "Output contains extra elements");
		sumpa += (k - 1LL) * a[i];
	}
	
	if (sumpa != m)
		quitf(_wa, "Participant sum not equal to m");

    quitf(_ok, ":)");
}