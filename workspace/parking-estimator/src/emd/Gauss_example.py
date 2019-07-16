import ot
import np

n_bins = 100

#gaussian = 10 * ot.datasets.make_1D_gauss(n_bins, m = 5, s = 2)
gaussian = np.zeros((n_bins))
gaussian += 2 * ot.datasets.make_1D_gauss(n_bins, m = 5, s = 2)
gaussian += 5 * ot.datasets.make_1D_gauss(n_bins, m = 50, s = 2)


volume = 0
sum = 0
for i in range(n_bins):
    print(str(gaussian[i]) + " ")
    volume += i*gaussian[i]
    sum += gaussian[i]

print("sum: " + str(sum))
print("volume: " + str(volume))
