import argparse
import socket


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='RITE')
parser.add_argument('--num_iterations', type=int, default=5)
parser.add_argument('--criterion', type=str, default='RRLoss')
parser.add_argument('--base_criterion', type=str, default='BCE3Loss')
parser.add_argument('--model', type=str, default='RRWNet')
parser.add_argument('--num_folds', type=int, default=4)
parser.add_argument('--learning_rate', type=float, default=1e-04)
parser.add_argument('--num_epochs', type=int, default=None)
parser.add_argument('--base_channels', type=int, default=64)
parser.add_argument('--in_channels', type=int, default=3)
parser.add_argument('--out_channels', type=int, default=3)
parser.add_argument('--gpu_id', type=int, default=0)
parser.add_argument('--n_proc', type=int, default=1)
parser.add_argument('--data_folder', type=str, default='./_Data/')
parser.add_argument('--version', type=str, default='Journal_paper')
parser.add_argument('--seed', type=int, default=77)
args = parser.parse_args()

### Configuration arguments

num_folds = args.num_folds
active_folds = range(num_folds)

learning_rate = args.learning_rate
num_epochs = args.num_epochs

dataset = args.dataset

model = args.model
in_channels = args.in_channels
out_channels = args.out_channels
if socket.gethostname() == 'hemingway':
    # Reduce the model size for local testing
    args.base_channels = 16
base_channels = args.base_channels
num_iterations = args.num_iterations

criterion = args.criterion
base_criterion = args.base_criterion

n_proc = args.n_proc
gpu_id = args.gpu_id

training_folder = f'__training/{args.version}/{dataset}'

seed = args.seed

if dataset == 'ECG':
    images = [
        '0_0', '0_1', '0_2', '0_3', '0_4', '0_5', '0_6', '0_7', '0_8', '0_9', '0_10', '0_11', '0_12', '0_13', '0_14', '0_15', '0_16', '0_17', '0_18', '0_19', '0_20', '0_21', '0_22', '0_23', '0_24', '0_25', '0_26', '0_27', '0_28', '0_29', '0_30', '0_31', '0_32', '0_33', '0_34', '0_35', '0_36', '0_37', '0_38', '0_39', '0_40', '0_41', '0_42', '0_43', '0_44', '0_45', '0_46', '0_47', '0_48', '0_49', '0_50', '0_51', '0_52', '0_53', '0_54', '0_55', '0_56', '0_57', '0_58', '0_59', '0_60', '0_61', '0_62', '0_63', '0_64', '0_65', '0_66', '0_67', '0_68', '0_69', '0_70', '0_71', '0_72', '0_73', '0_74', '0_75', '0_76', '0_77', '0_78', '0_79', '0_80', '0_81', '0_82', '0_83', '0_84', '0_85', '0_86', '0_87', '0_88', '0_89', '0_90', '0_91', '0_92', '0_93', '0_94', '0_95', '0_96', '0_97', '0_98', '0_99', '0_100', '0_101', '0_102', '0_103', '0_104', '0_105', '0_106', '0_107', '0_108', '0_109', '0_110', '0_111', '0_112', '0_113'
    ]
    data = {
        'data_folder': args.data_folder,
        'target': {
            'path': 'ECG/train/target',
            'pattern': r'.*\.png$'
        },
        'original': {
            'path': 'ECG/train/original',
            'pattern': r'.*\.png$'
        },
        'mask': {
            'path': 'ECG/train/mask',
            'pattern': r'.*\.png$'
        }
    }

elif dataset == 'RITE-train':
    images = [
        33, 24, 36, 30, 25, 29, 40, 21, 37, 34, 35, 32, 27, 39, 26, 38, 28, 23,
        31, 22
    ]
    data = {
        'data_folder': args.data_folder,
        'target': {
            'path': 'RITE/train/av3',
            'pattern': '[0-9]+[.]png'
        },
        'original': {
            'path': 'RITE/train/enhanced',
            'pattern': '[0-9]+[.]png'
        },
        'mask': {
            'path': 'RITE/train/enhanced_masks',
            'pattern': '[0-9]+[.]png'
        }
    }
elif dataset == 'HRF-Karlsson-w1024':
    images = [
        '06_dr', '06_g', '06_h', '07_dr', '07_g', '07_h', '08_dr', '08_g',
        '08_h', '09_dr', '09_g', '09_h', '10_dr', '10_g', '10_h', '11_dr',
        '11_g', '11_h', '12_dr', '12_g', '12_h', '13_dr', '13_g', '13_h',
        '14_dr', '14_g', '14_h', '15_dr', '15_g', '15_h',
    ]
    data = {
        'data_folder': args.data_folder,
        'target': {
            'path': f'HRF_AVLabel_191219/train_karlsson_w1024/av3',
            'pattern': '[0-9]+_.+[.]png'
        },
        'original': {
            'path': f'HRF_AVLabel_191219/train_karlsson_w1024/enhanced',
            'pattern': '[0-9]+_.+[.]png'
        },
        'mask': {
            'path': f'HRF_AVLabel_191219/train_karlsson_w1024/enhanced_masks',
            'pattern': '[0-9]+_.+[.]png'
        }
    }

else:
    raise ValueError('dataset not supported')

