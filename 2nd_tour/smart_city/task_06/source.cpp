#include <cstdio>
#include <string>
#include <cmath>
using namespace std;

FILE *f = nullptr;
FILE *fo = nullptr;

int sol()
{
    int a1, a2, a3, a4;
    fscanf(f, "%d%d%d%d", &a1, &a2, &a3, &a4);
    if (a3 > a1 || a3 > a2 || a4 > a1 || a4 > a2 || a3 - a4 > 1 || a4 - a3 > 1)
    {
        fprintf(fo, "-1\n");
        return 0;
    }
    string s;
    s = '3';
    --a1;
    int i = 0;
    while (a1&&a2&&a3&&a4)
    {
        if (s[i] == '3')
        {
            s += '9';
            --a2, --a3, ++i;
        }
        if (s[i] == '9')
        {
            s += '3';
            --a1, --a4, ++i;
        }
    }

    if (!a1)
    {
        if (s[s.length() - 1] == '3')
        {
            if ((!a2 && (a3 || a4)) || a3 > 1 || a4 > 1)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            if (a2 && a3 == 1)
            {
                s += '9';
                a3 = 0;
                --a2;
            }
            if (!a2 && a4)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            if (a2 && a4 == 1)
            {
                s = "9" + s;
                --a2;
                a4 = 0;
            }
            for (int i = 0; i < s.length(); ++i)
            {
                if (i + 1 == s.length())
                    for (int i = 0; i < a2; ++i)
                        fprintf(fo, "9");
                fprintf(fo, "%c", s[i]);
            }
            return 0;
        }
    }

    if (!a2)
    {
        if (s[s.length() - 1] == '3')
        {
            if (a3 || a4)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            return 0;
        }


        if (s[s.length() - 1] == '9')
        {
            if ((!a1 && (a3 || a4)) || a3 || a4 > 1)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            if (a1 && a4 == 1)
            {
                s += '3';
                --a1;
                a4 = 0;
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            return 0;
        }
    }

    if (!a3)
    {
        if (!a4)
        {
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            if (s[s.length() - 1] != '3')
            {
                fprintf(fo, "%s\n", s.c_str());
                for (int i = 0; i < a2; ++i)
                    fprintf(fo, "9");
            } else
            {
                for (int i = 0; i < s.length(); ++i)
                {
                    if (i + 1 == s.length())
                        for (int j = 0; j < a2; ++j)
                            fprintf(fo, "9");
                    fprintf(fo, "%c", s[i]);
                }

            }
            return 0;
        }

        if (s[s.length() - 1] == '3')
        {
            if ((a4 && !a2) || a4 > 1)
            {
                fprintf(fo, "-1\n");
                return 0;
            } else if (a4 == 1 && a2)
            {
                //s = "9" + s;
                --a2;
                --a4;
                fprintf(fo, "9");
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            for (int i = 0; i < s.length(); ++i)
            {
                if (i + 1 == s.length())
                    for (int j = 0; j < a2; ++j)
                        fprintf(fo, "9");
                fprintf(fo, "%c", s[i]);
            }
            return 0;

        }

        if (s[s.length() - 1] == '9')
        {
            if ((a4 && !a1) || a4 > 1)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            if (a4 == 1 && a1)
            {
                s += "3";
                --a1;
                --a4;
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            for (int j = 0; j < a2; ++j)
                fprintf(fo, "9");
            return 0;

        }
    }

    if (!a4)
    {
        if (!a3)
        {
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            for (int i = 0; i < a2; ++i)
                fprintf(fo, "9");
            return 0;
        }

        if (s[s.length() - 1] == '3')
        {
            if ((a3 && !a2) || a3 > 1)
            {
                fprintf(fo, "-1\n");
                return 0;
            } else if (a3 == 1 && a2)
            {
                s += "9";
                --a2;
                --a3;
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            for (int j = 0; j < a2; ++j)
                fprintf(fo, "9");
            return 0;

        }

        if (s[s.length() - 1] == '9')
        {
            if (a3)
            {
                fprintf(fo, "-1\n");
                return 0;
            }
            for (int i = 0; i < a1; ++i)
                fprintf(fo, "3");
            fprintf(fo, "%s\n", s.c_str());
            for (int i = 0; i < a2; ++i)
                fprintf(fo, "9");
            return 0;

        }
    }
}

int main()
{
    f = stdin;
    fo = stdout;
    sol();
    return 0;
}