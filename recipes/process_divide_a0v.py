import astropy.io.fits as pyfits
import numpy as np

from libs.a0v_spec import A0V


def generate_a0v_divided(helper, band, obsids):

    caldb = helper.get_caldb()

    master_obsid = obsids[0]
    tgt_spec_hdulist = caldb.load_item_from((band, master_obsid),
                                            "SPEC_FITS")
    spec = tgt_spec_hdulist[0].data
    wvl = tgt_spec_hdulist[1].data

    a0v_basename = caldb.db_query_basename("a0v", band, master_obsid)

    a0v_spec_hdulist = caldb.load_item_from(a0v_basename,
                                            "SPEC_FITS")

    a0v_spec = a0v_spec_hdulist[0].data

    a0v_interp1d = A0V.get_flux_interp1d(helper.config)
    vega = np.array([a0v_interp1d(w1) for w1 in wvl])

    master_hdu = tgt_spec_hdulist[0]

    basename = helper.get_basename(band, master_obsid)

    store_tgt_divide_a0v(caldb, basename,
                         master_hdu,
                         wvl, spec, a0v_spec, vega)


def store_tgt_divide_a0v(caldb, basename,
                         master_hdu,
                         wvl, spec, a0v_spec, vega):

    from libs.products import PipelineImage as Image
    from libs.products import PipelineImages

    image_list = [Image([("EXTNAME", "SPEC_DIVIDE_A0V")],
                        spec/a0v_spec*vega)]
    image_list.append(Image([("EXTNAME", "WAVELENGTH")],
                            wvl))
    image_list.append(Image([("EXTNAME", "TGT_SPEC")],
                            spec))
    image_list.append(Image([("EXTNAME", "A0V_SPEC")],
                            a0v_spec))
    image_list.append(Image([("EXTNAME", "VEGA_SPEC")],
                            vega))


    product = PipelineImages(image_list, masterhdu=master_hdu)
    item_type = "SPEC_A0V_FITS"
    item_desc = caldb.DESC_DICT[item_type.upper()]
    caldb.helper.igr_storage.store_item(item_desc, basename,
                                        product)




if 0:
    hdulist = pyfits.open("/home/jjlee/work/igrins/plp_jjlee/outdata/20140525/SDCK_20140525_0042.spec_a0v.fits")

    s = hdulist["SPEC_DIVIDE_A0V"].data
    wvl = hdulist["WAVELENGTH"].data
    tgt_s = hdulist["TGT_SPEC"].data
    a0v_s = hdulist["A0V_SPEC"].data
    vega_s = hdulist["VEGA_SPEC"].data

    clf()
    m = np.median(a0v_s)
    for w1, s1, a0v1 in zip(wvl, s, a0v_s):
        s1 = np.ma.array(s1, mask=a0v1<0.3*m).filled(np.nan)
        plot(w1, s1)

from libs.recipe_helper import RecipeHelper

def process_band(utdate, recipe_name, band, obsids, config_name):

    helper = RecipeHelper(config_name, utdate, recipe_name)

    generate_a0v_divided(helper, band, obsids)


if __name__ == "__main__":

    recipe_name = "divide_a0v"
    utdate = "20140525"
    obsids = [42]

    band = "K"

    config_name = "../recipe.config"

    process_band(utdate, recipe_name, band, obsids, config_name)
