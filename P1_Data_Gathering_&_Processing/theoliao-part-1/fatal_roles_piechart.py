import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1,2,sharey = True, figsize=(9, 5))

types = ["Driver","Passenger","Pedestrian"]
data_france = [35129,8744,6716]
data_uk = [14924,4284,5594]


def func(x, allvals):
    absolute =int((x * np.sum(allvals))/100+0.5) # +0.5 to prevent rounding
    return "{:.1f}%\n({:d})".format(x,absolute)


wedges1, texts1, autotexts1 = ax1.pie(data_france, autopct=lambda x: func(x, data_france),
                                  textprops=dict(color="w"))
wedges2, texts2, autotexts2 = ax2.pie(data_uk, autopct=lambda x: func(x, data_uk),
                                  textprops=dict(color="w"))

ax1.legend(wedges1, types,
          title="Roles",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts1, size=8, weight="bold")
plt.setp(autotexts2, size=8, weight="bold")

ax1.set_title("The dead in France")
ax2.set_title("The dead in the U.K.")

plt.show()