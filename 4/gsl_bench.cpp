#include <iostream>
#include <iomanip>
#include <fstream>
#include <chrono>
#include <string>
#include <vector>
#include <cmath>

#include <gsl/gsl_rng.h>

using moment = std::chrono::steady_clock::time_point;
moment teraz() { return std::chrono::steady_clock::now(); }
long ile_trwa(moment a, moment b) {
    return std::chrono::duration_cast<std::chrono::microseconds>(b - a).count();
}

double measure(const gsl_rng *r, long n) {
    double acc = 0.0;
    moment t0 = teraz();
    for (long i = 0; i < n; ++i) {
        acc += gsl_rng_uniform(r);   // liczba z [0,1)
    }
    moment t1 = teraz();
    if (acc == -1.0) std::cerr << "unreachable\n";
    return ile_trwa(t0, t1) / 1000.0;
}

int main() {
    const gsl_rng_type **t, **t0;
    t0 = gsl_rng_types_setup();

    unsigned long seed = 123456789UL;

    const gsl_rng_type *T_default = gsl_rng_default;
    gsl_rng *r_default = gsl_rng_alloc(T_default);
    gsl_rng_set(r_default, seed);

    const double target_ms = 500.0;
    long n_default = 10000000L;
    double t_default = 0.0;
    while (true) {
        t_default = measure(r_default, n_default);
        if (t_default >= target_ms) break;
        n_default *= 2;
        if (n_default > 1000000000L) break;
    }
    gsl_rng_free(r_default);

    std::cout << "Generator domyślny ("
              << gsl_rng_name(gsl_rng_alloc(T_default)) << ")"
              << ": n = " << n_default
              << ", t = " << std::fixed << std::setprecision(1)
              << t_default << " ms\n\n";

    std::ofstream out("czasy_gsl.txt");
    out << "# generator  n  time_ms  time_norm\n";

    std::cout << std::left
              << std::setw(22) << "generator"
              << std::setw(14) << "n"
              << std::setw(12) << "t [ms]"
              << "t/t_default\n";
    std::cout << std::string(60, '-') << "\n";

    for (t = t0; *t != nullptr; ++t) {
        const char *name = (*t)->name;
        gsl_rng *r = gsl_rng_alloc(*t);
        gsl_rng_set(r, seed);

        long n = n_default;
        double t_ms = 0.0;
        while (true) {
            t_ms = measure(r, n);
            if (t_ms >= target_ms || n >= 1000000000L) break;
            n *= 2;
        }

        double norm = t_ms / t_default;

        std::cout << std::left << std::setw(22) << name
                  << std::setw(14) << n
                  << std::fixed << std::setprecision(1)
                  << std::setw(12) << t_ms
                  << std::setprecision(3) << norm << "\n";

        out << name << " " << n << " "
            << std::fixed << std::setprecision(3) << t_ms << " "
            << std::setprecision(6) << norm << "\n";

        gsl_rng_free(r);
    }

    out.close();
    std::cout << "\nDane zapisano do pliku: czasy_gsl.txt\n";
    return 0;
}

// g++ -std=c++11 -o gsl_bench gsl_bench.cpp -lgsl -lm
