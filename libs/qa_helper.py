def figlist_to_pngs(rootname, figlist, postfixes=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from itertools import izip, count

    if postfixes is None:
        postfixes = ("fig%02d" % i for i in count(1))

    for postfix, fig in izip(postfixes, figlist):
        FigureCanvasAgg(fig)
        fig.savefig("%s_%s.png" % (rootname, postfix))
        #fig2.savefig("align_zemax_%s_fig2_fit.png" % postfix)
        #fig3.savefig("align_zemax_%s_fig3_hist_dlambda.png" % postfix)
