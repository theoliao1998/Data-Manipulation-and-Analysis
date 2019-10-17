(12, 0.016736902237469008)
(13, 0.01645516128619175)
(14, 0.016322632192810327)
(15, 0.01688742035651221)
(5, 0.01866322316254549)
(6, 0.018213693267398297)
(7, 0.01784351166911564)
(8, 0.01737150535627636)
(9, 0.017173054922856524)
(10, 0.016596847095138353)
(11, 0.01705565784285078)

year = range(2005,2016)
rate = [0.01866322316254549, 0.018213693267398297, 0.01784351166911564, 0.01737150535627636, 0.017173054922856524, \
     0.016596847095138353, 0.01705565784285078,0.016736902237469008, 0.01645516128619175, 0.016322632192810327, 0.01688742035651221]

import matplotlib.pyplot as plt

plt.plot(year,rate,'xr--')
plt.xlabel("Year")
plt.ylabel("Overall fatal rate (in France and the Uk)")
plt.xticks(year)
plt.show()