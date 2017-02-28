
def q2_plot():
    plt.clf() #clears plot
    ydata = [1 for i in range(10)] + [2 for i in range(10)] + [3 for i in range(10)]+ [4 for i in range(10)]+ [5 for i in range(10)]
    random = [1, 10, 100, 20000, 10000, 100000, 500000, 700000, 1000000, 5000000]
    pa = [1, 3000, 100, 1000, 2000, 100000, 500000, 700000, 1000000, 5000000]
    group = [10, 10000, 100, 1000, 30000, 100000, 500000, 10000000, 1000000, 5000000]
    ws = [1000, 10000, 100, 1000, 10000, 100000, 500000, 200000, 1000000, 5000000]
    coauthorship = [5, 10, 100, 1000, 50000, 100000, 500000, 700000, 1000000, 5000000]
    xdata = random + pa + group + ws + coauthorship
    plt.ylim(0,6)
    plt.yticks((1, 2, 3, 4, 5), ('Random', 'PA', 'Group', 'WS', 'Coauthorship'))
    plt.semilogx(xdata, ydata, marker='.', linestyle = 'None', color='b')
    plt.savefig("example.png")


            
