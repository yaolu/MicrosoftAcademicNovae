f=open('pub_number_first_author.csv').readlines()
f = [int(elem.strip('\n').split('\t')[1]) for elem in f]
pub_num = f
from scipy.stats.kde import gaussian_kde
kde = gaussian_kde( pub_num)
from matplotlib import pyplot as plt
import numpy as np
dist_space = np.linspace( min(pub_num), max(pub_num), 100 )
plt.plot( dist_space, kde(dist_space))
plt.title('Publication Numbers Distribution in *ACL')
plt.xlabel('Number of Publications')
plt.ylabel('Probability')
plt.plot( dist_space, kde(dist_space))
plt.savefig('/tmp/aa.pdf')
