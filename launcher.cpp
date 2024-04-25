#include<windows.h>
using namespace std;
int main()
{
    system("start cmd.exe /c python source/server_listen.py");
    system("start cmd.exe /c python source/client_start.py");
}