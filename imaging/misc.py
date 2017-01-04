def pull_data(source=None):
    from csxdata import roots
    from csxdata.utilities.highlevel import image_sequence_to_array

    source = roots["ntabpics"] if source is None else source
    return image_sequence_to_array(source, outpath=roots["cache"] + "ntabpics.npa", generator=1)
