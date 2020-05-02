#include <iostream>
#include <chrono>
#include <ctime>
#include <vector>

using namespace std;
extern "C" int square(int x){
    return x*x;
}

extern "C" [[maybe_unused]] vector<string> actions(const vector<string>& reddit)
{
    vector<string> actions;
    actions.reserve(reddit.size());
    for (auto const& action: reddit)
    {
        actions.push_back(action);
    }

    return actions;
}

typedef std::chrono::system_clock Clock;

int main()
{
    using namespace std;
    using namespace std::chrono;
    typedef duration<int, ratio_multiply<hours::period, ratio<24> >::type> days;
    system_clock::time_point now = system_clock::now();
    system_clock::duration tp = now.time_since_epoch();
    days d = duration_cast<days>(tp);
    tp -= d;
    hours h = duration_cast<hours>(tp);
    tp -= h;
    minutes m = duration_cast<minutes>(tp);
    tp -= m;
    seconds s = duration_cast<seconds>(tp);
    tp -= s;
    std::cout << d.count() << "d " << h.count() << ':'
              << m.count() << ':' << s.count();
    std::cout << " " << tp.count() << "["
              << system_clock::duration::period::num << '/'
              << system_clock::duration::period::den << "]\n";

    time_t tt = system_clock::to_time_t(now);
    tm utc_tm = *gmtime(&tt);
    tm local_tm = *localtime(&tt);
    std::cout << utc_tm.tm_year + 1900 << '-';
    std::cout << utc_tm.tm_mon + 1 << '-';
    std::cout << utc_tm.tm_mday << ' ';
    std::cout << utc_tm.tm_hour << ':';
    std::cout << utc_tm.tm_min << ':';
    std::cout << utc_tm.tm_sec << '\n';
}