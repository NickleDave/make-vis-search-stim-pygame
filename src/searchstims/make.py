import json
import pygame

from . import stim_makers


def make(config_tuple):
    """actual function that makes all the stimuli

    Parameters
    ----------
    config_tuple : ConfigTuple
        returned by parse_config after parsing a config.ini file

    Returns
    -------
    None

    saves all the stimuli to config_tuple.output_dir
    """
    if not os.path.isdir(config_tuple.output_dir):
        os.makedirs(config_tuple.output_dir)
    # put filenames in a dict that we save as json
    # so we don't have to do a bunch of string matching to find them later,
    # instead we can just get all the filenames for a given set size
    # with target present or absent
    # by using appropriate keys
    # e.g. fnames_set_size_8_target_present = filenames_dict[8]['present']
    filenames_dict = {}
    general_config = config_tuple.general
    if general_config.stimulus == 'rectangle':
        stim_maker = stim_makers.RectangleStimMaker()
    elif general_config.stimulus == 'number':
        stim_maker = stim_makers.NumberStimMaker()

    for set_size in general_config.set_sizes:
        # add dict for this set size that will have list of "target present / absent" filenames
        filenames_dict[set_size] = {}

        if not os.path.isdir(
            os.path.join(general_config.output_dir, str(set_size))
        ):
            os.makedirs(
                os.path.join(general_config.output_dir, str(set_size))
            )
        for target in ('present', 'absent'):
            # add the actual filename list for 'present' or 'absent'
            filenames_dict[set_size][target] = []
            if target == 'present':
                inds_of_stim_to_make = range(general_config.num_target_present // len(general_config.set_sizes))
                num_target = 1
            elif target == 'absent':
                inds_of_stim_to_make = range(general_config.num_target_absent // len(general_config.set_sizes))
                num_target = 0

            if not os.path.isdir(
                    os.path.join(general_config.output_dir, str(set_size), target)
            ):
                os.makedirs(os.path.join(general_config.output_dir, str(set_size), target))

            for i in inds_of_stim_to_make:
                if general_config.stimulus == 'rectangle':
                    filename = ('redvert_v_greenvert_set_size_{}_'
                                'target_{}_{}.png'.format(set_size, target, i))
                elif general_config.stimulus == 'number':
                    filename = ('two_v_five_set_size_{}_'
                                'target_{}_{}.png'.format(set_size, target, i))
                surface = stim_maker.make_stim(set_size=set_size,
                                               num_target=num_target)
                filename = os.path.join(config_tuple.output_dir,
                                        str(set_size),
                                        target,
                                        filename)
                pygame.image.save(surface, filename)
                filenames_dict[set_size][target].append(filename)

    filenames_json = json.dumps(filenames_dict, indent=4)
    with open(config_tuple.json_filename, 'w') as json_output:
        print(filenames_json, file=json_output)
