import matplotlib.pyplot as plt
import numpy as np
year = np.arange(2005,2016)
data_f = [5543, 4942, 4838, 4443, 4443, 4172, 4111, 3842, 3427, 3557, 3616]
data_uk = [3201, 3172, 2946, 2538, 2222, 1850, 1901, 1754, 1713, 1775, 1730]

width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(year - width/2, data_f, width, label='France')
rects2 = ax.bar(year + width/2, data_uk, width, label='UK')

ax.set_xlabel('Year')
ax.set_title('Number of people dead in accidents')
ax.set_xticks(year)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()
