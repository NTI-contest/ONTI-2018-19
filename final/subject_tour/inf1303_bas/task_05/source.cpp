#include <cstdio>
#include <string>
#include <iostream>
#include <list>
#include <utility>

int main()
{
    int x = 0;
    std::string line = "";
    std::list<int> repeats_count;
    repeats_count.push_back(1);
    int current_block = 0;

    while (line != "END")
    {
        std::getline(std::cin, line);
        std::string command = line.substr(0, 3);

        if (command == "END")
            break;
        else if (command == "REP")
            repeats_count.push_back(atoi(line.substr(4, line.size() - 4).c_str()) 
            * repeats_count.back());
        else if (command == "BLB")
        {
            current_block++;
        }
        else if (command == "BLE")
        {
            repeats_count.pop_back();
            current_block--;
        }
        else
        {
            int jump = atoi(line.substr(4, line.size() - 4).c_str());
            if (repeats_count.size() != 0)
                x += jump * repeats_count.back();
            else
                x += jump;
        }
    }
    std::cout << x;
}