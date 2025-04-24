import matplotlib.pyplot as plt


def plot_free_energy_difference(methods, ns, dates, base_dir):
    plt.figure(figsize=(10, 6))
    dat_num = 21
    # dat_num = 101
    times = np.linspace(0,20,dat_num)
    for method,date in zip(methods,dates):
        seed_delta_fs = []
        for seed in range(1):
            delta_fs = []
            for i in range(dat_num):
                fes_dir = os.path.join(base_dir, method, ns, 'log', date, str(seed))
                if method in ['phi','ref']:
                    phi, free = load_data(fes_dir, method, i)
                else:
                    phi, free = load_interp(fes_dir, method, i)
                delta_f = calculate_delta_f(phi, free)
                delta_fs.append(delta_f)
            seed_delta_fs.append(delta_fs)

        delta_fs = np.array(seed_delta_fs)
        mean_delta_fs = np.nanmean(delta_fs, axis=0)
        std_delta_fs = np.nanstd(delta_fs, axis=0)

        c = colors.pop(0)
        mask = ~np.isnan(mean_delta_fs)
        if mask.sum() == 0:
            plt.plot(times, np.zeros_like(times), label=f'{method}=NaN', alpha=0.0)
        else:
            plt.plot(times[mask], mean_delta_fs[mask], label=f'{method}', color=c)
            plt.fill_between(times[mask], mean_delta_fs[mask] - std_delta_fs[mask], mean_delta_fs[mask] + std_delta_fs[mask], alpha=0.2, color=c)

    plt.xlim(0,20)
    plt.ylim(-20,50)
    plt.axhline(y=9.04, color='r', linestyle='--', label='GT')
    plt.fill_between(times, 9.04 - 0.33, 9.04 + 0.33, color='r', alpha=0.2)
    plt.xlabel('Time (ns)', fontsize=20, fontweight="medium")
    plt.ylabel(r'$\Delta F$'+' (kJ/mol)', fontsize=20, fontweight="medium")
    plt.legend(fontsize=8, loc='best')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'./fig/delta_{methods[0]}_{ns}.pdf', dpi=300, bbox_inches="tight")
    plt.savefig(f'./fig/delta_{methods[0]}_{ns}.png', dpi=300, bbox_inches="tight")
    print(f'Figure saved at ./fig/delta_{methods[0]}_{ns}.pdf')
    plt.show()
    plt.close()