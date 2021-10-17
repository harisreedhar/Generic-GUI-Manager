projects = {}

# Sim Swap configuration
projects['Sim Swap'] = {
    'project directory': '/home/hari/Apps/SimSwap/SimSwap-main/', # project directory to run python from
    'file path': '/home/hari/Apps/SimSwap/SimSwap-main/test_video_swapmulti.py', # file to run
    'python path': '/home/hari/anaconda3/envs/simswap/bin/python', # python env
    'inputs': [
        # {index, name, type:(FILE || DIRECTORY || STRING), value: default value}
        {'index': 0, 'name':'Arc Path', 'type':'DIRECTORY', 'value':'/home/hari/Apps/SimSwap/SimSwap-main/arcface_model/arcface_checkpoint.tar'},
        {'index': 1, 'name':'Face Image', 'type':'FILE', 'value':''},
        {'index': 2, 'name':'Video File', 'type':'FILE', 'value':''},
        {'index': 3, 'name':'Output Dir', 'type':'DIRECTORY', 'value':''},
        {'index': 4, 'name':'Temp path', 'type':'DIRECTORY', 'value':'/home/hari/Apps/SimSwap/SimSwap-main/temp_results'},
        {'index': 5, 'name':'Other Arguments', 'type':'STRING', 'value':'--isTrain false --use_mask --name people'},
    ],
    'splitted command': [ # should be in same order as inputs
        '--Arc_path', #index 0 arc path
        '--pic_a_path', # index 1 pic path
        '--video_path', # index 2 video path
        '--output_path', # index 3 output directory
        '--temp_path', # index 4 temp path
        '', # index 5 other arguments
    ],
}

projects["Wav 2 Lip"] = {
    'project directory': "/home/hari/Apps/Wav2Lip-master",
    'file path': "/home/hari/Apps/Wav2Lip-master/inference.py",
    'python path': "/home/hari/anaconda3/envs/wav2lip/bin/python",
    'inputs': [
        {'index': 0, 'name':'Check Point', 'type':'FILE', 'value':'/mnt/95d2aa3d-99e9-4600-91b1-2fcecff0dec5/AI_Tools/Wav2Lip/requirements/wav2lip.pth'},
        {'index': 1, 'name':'Source Video', 'type':'FILE', 'value':''},
        {'index': 3, 'name':'Source Audio', 'type':'FILE', 'value':''},
        {'index': 4, 'name':'Output', 'type':'DIRECTORY', 'value':''},
        {'index': 5, 'name':'Other Arguments', 'type':'STRING', 'value':'--pads 0 20 0 0 --nosmooth'}
    ],
    'splitted command': [
        '--checkpoint_path',
        '--face',
        '--audio',
        '--outfile',
        '',
    ]
}
