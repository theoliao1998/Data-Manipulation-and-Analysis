"""
output for lighting_effects.py 

Light_Conditions,Accident_Severity,cnt
1,1,39866
1,2,382904
1,3,1458565
4,1,9944
4,2,99855
4,3,381208
5,1,635
5,2,3895
5,3,10549
6,1,15684
6,2,54526
6,3,94548

where Light_Conditions means
code	label
1	Daylight
4	Darkness - lights lit
5	Darkness - lights unlit
6	Darkness - no public lighting

and Accident_Severity means
code	label
1	Fatal
2	Serious
3	Slight

"""
import numpy as np
import matplotlib.pyplot as plt


category_names = ['Fatal', 'Serious','Slight']
original_data = {
    'Daylight': np.array([39866,382904,1458565]),
    'Darkness -\n lights lit': np.array([9944,99855,381208]),
    'Darkness -\n lights unlit': np.array([635,3895,10549]),
    'Darkness -\n no public lighting': np.array([15684,54526,94548])
}

data = {k:original_data[k]/np.sum(original_data[k])*100  for k in original_data}


def survey(results, category_names):

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'black'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, ("%.2f" % c + '%'), ha='center', va='center',
                    color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax


survey(data, category_names)
plt.show()