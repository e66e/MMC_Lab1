#include <iostream>
#include <iomanip>
#include <fstream>
#include <random>
#include <chrono>
#include <string>

typedef std::chrono::steady_clock::time_point moment;
moment teraz() { return std::chrono::steady_clock::now(); }
long ile_trwa(moment od_kiedy, moment do_kiedy) {
    return std::chrono::duration_cast<std::chrono::microseconds>(
               do_kiedy - od_kiedy).count();
}

template <class Engine>
long measure(Engine& gen, long n, double& checksum) {
    std::uniform_real_distribution<double> dist(0.0, 10.0);
    double acc = 0.0;
    moment t0 = teraz();
    for (long i = 0; i < n; ++i) {
        double v = dist(gen);
        acc += v;
    }
    moment t1 = teraz();
    checksum = acc;
    return ile_trwa(t0, t1);
}

template <class Engine>
void run_engine(const std::string& name,
                std::ofstream& out,
                bool fixed_seed,
                unsigned long long seedval)
{
    typename Engine::result_type seed;
    if (fixed_seed) {
        seed = static_cast<typename Engine::result_type>(seedval);
    } else {
        std::random_device rd;
        seed = static_cast<typename Engine::result_type>(
            (static_cast<unsigned long long>(rd()) << 32) ^ rd());
    }
    if (seed == 0) seed = 1;

    Engine gen(seed);

    const long target_us = 500000;
    long n = 1000000L;
    long t_us = 0;
    double checksum = 0.0;

    while (true) {
        t_us = measure(gen, n, checksum);
        if (t_us >= target_us) break;
        n *= 2;
        if (n > (1L << 34)) break;
    }

    double t_ms = t_us / 1000.0;

    std::cout << std::left << std::setw(15) << name
              << "  n = " << std::setw(11) << n
              << "  t = " << std::fixed << std::setprecision(1)
              << std::setw(9) << t_ms << " ms"
              << "  checksum = " << std::setprecision(6) << checksum
              << "\n";

    out << name << " " << n << " " << std::setprecision(3) << t_ms
        << " " << std::setprecision(17) << checksum << "\n";
}

int main(int argc, char** argv) {
    bool fixed_seed = (argc > 1 && std::string(argv[1]) == "--fixed");
    unsigned long long seedval = 123456789ULL;

    std::ofstream out("czasy.txt");
    out << "# generator n time_ms checksum\n";

    std::cout << "Ziarno: "
              << (fixed_seed ? "USTALONE (" + std::to_string(seedval) + ")"
                             : std::string("random_device"))
              << "\n\n";

    run_engine<std::minstd_rand>  ("minstd_rand",   out, fixed_seed, seedval);
    run_engine<std::mt19937>      ("mt19937",       out, fixed_seed, seedval);
    run_engine<std::mt19937_64>   ("mt19937_64",    out, fixed_seed, seedval);
    run_engine<std::ranlux48_base>("ranlux48_base", out, fixed_seed, seedval);
    run_engine<std::ranlux48>     ("ranlux48",      out, fixed_seed, seedval);
    run_engine<std::knuth_b>      ("knuth_b",       out, fixed_seed, seedval);

    return 0;
}

// g++ -std=c++11 -o pomiar pomiar.cpp