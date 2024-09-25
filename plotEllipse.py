import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import pandas as pd
import seaborn as sns

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The Axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

fig, ax_kwargs = plt.subplots(figsize=(6, 6))
dependency_kwargs = [[-0.8, 0.5],
                     [-0.2, 0.5]]
mu = 2, -3
scale = 6, 5

file_path = 'Gait Analysis_Brick.xlsx' # Change file name as needed
B = str(file_path).split('_')[1].split('.')[0]
ax_kwargs.set_title(B.upper())
sheet_name = 'Consolidated'
df = pd.read_excel(file_path, sheet_name=sheet_name, usecols='D:I', skiprows=1)

sns.set_style("darkgrid") #Options: deep, muted, bright, pastel, dark, colorblind

# Plt the mean with cross mark
#ax_kwargs.scatter(df['Del X1'].mean(), df['Del Y1'].mean(), c='blue', s=3, marker='x')

sns.scatterplot(x='Del X1', y='Del Y1', data=df, ax=ax_kwargs,color=[117/255, 174/255, 148/255],label='0ML')

confidence_ellipse(df['Del X2'], df['Del Y2'], ax_kwargs,
                   alpha=0.2, facecolor=[189/255, 192/255, 190/255], edgecolor='white', zorder=0,label='_nolegend_')
sns.scatterplot(x='Del X2', y='Del Y2', data=df, ax=ax_kwargs, color=[189/255, 192/255, 190/255],label='1ML')

confidence_ellipse(df['Del X3'], df['Del Y3'], ax_kwargs,
                   alpha=0.2, facecolor=[178/255, 87/255, 81/255], edgecolor='red', zorder=0,label='_nolegend_')
sns.scatterplot(x='Del X3', y='Del Y3', data=df, ax=ax_kwargs,color=[178/255, 87/255, 81/255],label='2ML')

confidence_ellipse(df['Del X1'], df['Del Y1'], ax_kwargs,
                   alpha=1, facecolor=[117/255, 174/255, 148/255], edgecolor='blue', zorder=0, label='_nolegend_')


# Change legend order
# handles, labels = ax_kwargs.get_legend_handles_labels()
# h0 = handles[0]
# h2 = handles[1]
# h1 = handles[2]
# l1 = labels[0]
# l2 = labels[1]
# l0 = labels[2]
# new_order = ['0ML', '1ML', '2ML']
# ax_kwargs.legend([h0,h2,h1], [l0,l2,l1])
# handles, labels = plt.get_legend_handles_labels()
# handle_dict = dict(zip(labels, handles))
# new_handles = [handle_dict[label] for label in new_order]
# plt.legend(handles=new_handles, labels=new_order)
# plt.legend()

# axis title
ax_kwargs.set_xlabel('$\Delta$ X') 
ax_kwargs.set_ylabel('$\Delta$ Y')

# bold the axis title
ax_kwargs.xaxis.label.set_fontweight('bold')
ax_kwargs.yaxis.label.set_fontweight('bold')

# increase font size
ax_kwargs.xaxis.label.set_fontsize(26)
ax_kwargs.yaxis.label.set_fontsize(26)

# increase the legend size
ax_kwargs.legend(fontsize=20)

# Increase tick size
ax_kwargs.tick_params(axis='both', which='major', labelsize=24)

# Increase the title size
ax_kwargs.title.set_fontsize(20)
ax_kwargs.title.set_fontweight('bold')

# increase number of ticks
ax_kwargs.locator_params(axis='x', nbins=6)
ax_kwargs.locator_params(axis='y', nbins=6)

ax_kwargs.axvline(c='grey', lw=0.5)
ax_kwargs.axhline(c='grey', lw=0.5)

#legend = plt.legend(title='Robots', loc='upper left', frameon=True, shadow=True, borderpad=1)
plt.show()