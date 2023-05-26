from pathlib import Path
from fastsurfer import Segment, Noccseg, N4BiasCorrect, TalairachAndNu, UpdateAseg, SampleSegmentationToSurfave
from nipype import Node
import os
from run import set_envrion


def Segment_test():
    pwd = Path.cwd()  # 当前目录,# get FastSurfer dir Absolute path
    fastsurfer_home = pwd.parent / "FastSurfer"
    fastsurfer_eval = fastsurfer_home / 'FastSurferCNN' / 'eval.py'  # inference script
    weight_dir = fastsurfer_home / 'checkpoints'  # model checkpoints dir

    subjects_dir = Path("/mnt/ngshare/Data_Mirror/pipeline_test")
    subject_id = "sub-MSC01"
    os.environ['SUBJECTS_DIR'] = str(subjects_dir)

    network_sagittal_path = weight_dir / "Sagittal_Weights_FastSurferCNN" / "ckpts" / "Epoch_30_training_state.pkl"
    network_coronal_path = weight_dir / "Coronal_Weights_FastSurferCNN" / "ckpts" / "Epoch_30_training_state.pkl"
    network_axial_path = weight_dir / "Axial_Weights_FastSurferCNN" / "ckpts" / "Epoch_30_training_state.pkl"

    segment_node = Node(Segment(), f'segment_node')
    segment_node.inputs.python_interpret = '/home/anning/miniconda3/envs/3.8/bin/python3'
    segment_node.inputs.in_file = subjects_dir / subject_id / "mri" / "orig.mgz"
    segment_node.inputs.eval_py = fastsurfer_eval
    segment_node.inputs.network_sagittal_path = network_sagittal_path
    segment_node.inputs.network_coronal_path = network_coronal_path
    segment_node.inputs.network_axial_path = network_axial_path

    segment_node.inputs.aparc_DKTatlas_aseg_deep = subjects_dir / subject_id / "mri" / "aparc.DKTatlas+aseg.deep.mgz"
    segment_node.inputs.aparc_DKTatlas_aseg_orig = subjects_dir / subject_id / "mri" / "aparc.DKTatlas+aseg.orig.mgz"

    segment_node.inputs.conformed_file = subjects_dir / subject_id / "mri" / "conformed.mgz"
    segment_node.run()


def Noccseg_test():
    pwd = Path.cwd()  # 当前目录,# get FastSurfer dir Absolute path
    fastsurfer_home = pwd.parent / "FastSurfer"
    reduce_to_aseg_py = fastsurfer_home / 'recon_surf' / 'reduce_to_aseg.py'

    subjects_dir = Path('/mnt/ngshare/Data_Mirror/pipeline_test')
    subject_id = "sub-MSC01"
    os.environ['SUBJECTS_DIR'] = str(subjects_dir)

    noccseg_node = Node(Noccseg(), f'noccseg_node')
    noccseg_node.inputs.python_interpret = '/home/anning/miniconda3/envs/3.8/bin/python3'
    noccseg_node.inputs.reduce_to_aseg_py = reduce_to_aseg_py
    noccseg_node.inputs.in_file = subjects_dir / subject_id / "mri" / "aparc.DKTatlas+aseg.deep.mgz"

    noccseg_node.inputs.mask_file = subjects_dir / subject_id / 'mri/mask.mgz'
    noccseg_node.inputs.aseg_noCCseg_file = subjects_dir / subject_id / 'mri/aseg.auto_noCCseg.mgz'

    noccseg_node.run()


def N4_bias_correct_test():

    subjects_dir = Path("/mnt/ngshare/Data_Mirror/pipeline_test")
    subject_id = "sub-MSC01"
    sub_mri_dir = subjects_dir / subject_id / "mri"

    fastsurfer_home = Path("/") / "FastSurfer"
    correct_py = fastsurfer_home / "recon_surf" / "N4_bias_correct.py"

    orig_file = sub_mri_dir / "orig.mgz"
    mask_file = sub_mri_dir / "mask.mgz"

    orig_nu_file = sub_mri_dir / "orig_nu.mgz"

    N4_bias_correct_node = Node(N4BiasCorrect(), name="N4_bias_correct_node")
    N4_bias_correct_node.inputs.python_interpret = '/home/anning/miniconda3/envs/3.8/bin/python3'
    N4_bias_correct_node.inputs.correct_py = correct_py
    N4_bias_correct_node.inputs.orig_file = orig_file
    N4_bias_correct_node.inputs.mask_file = mask_file

    N4_bias_correct_node.inputs.orig_nu_file = orig_nu_file
    N4_bias_correct_node.inputs.threads = 8

    res = N4_bias_correct_node.run()
    res = res


def talairach_and_nu_test():
    subjects_dir = Path("/mnt/ngshare/Data_Mirror/pipeline_test")
    subject_id = "sub-MSC01"

    subjects_dir = Path('/mnt/ngshare/Data_Mirror/pipeline_test')
    subject_id = 'sub-MSC01'

    sub_mri_dir = subjects_dir / subject_id / "mri"

    orig_nu_file = sub_mri_dir / "orig_nu.mgz"
    orig_file = sub_mri_dir / "orig.mgz"

    talairach_lta = sub_mri_dir / "transforms" / "talairach.lta"
    nu_file = sub_mri_dir / "nu.mgz"

    freesurfer_home = Path(os.environ['FREESURFER_HOME'])
    mni305 = freesurfer_home / "average" / "mni305.cor.mgz"

    talairach_and_nu_node = Node(TalairachAndNu(), name="talairach_and_nu_node")
    talairach_and_nu_node.inputs.subjects_dir = subjects_dir
    talairach_and_nu_node.inputs.subject_id = subject_id
    talairach_and_nu_node.inputs.threads = 8
    talairach_and_nu_node.inputs.mni305 = mni305
    talairach_and_nu_node.inputs.orig_nu_file = orig_nu_file
    talairach_and_nu_node.inputs.orig_file = orig_file

    talairach_and_nu_node.inputs.talairach_lta = talairach_lta
    talairach_and_nu_node.inputs.nu_file = nu_file

    talairach_and_nu_node.run()


def UpdateAseg_test():
    subjects_dir = Path(f'/mnt/ngshare/DeepPrep/MSC/derivatives/deepprep/Recon')
    subjects_dir = Path('/mnt/ngshare/Data_Mirror/pipeline_test')
    subject_id = 'sub-MSC01'
    subject_mri_dir = subjects_dir / subject_id / 'mri'
    os.environ['SUBJECTS_DIR'] = str(subjects_dir)


    # subjects_dir = Path('/mnt/ngshare/DeepPrep_flowtest/V001/derivatives/deepprep/Recon')
    # subject_id = 'sub-001'
    # os.environ['SUBJECTS_DIR'] = str(subjects_dir)


    paint_cc_file = Path.cwd().parent / 'FastSurfer' / 'recon_surf' / 'paint_cc_into_pred.py'
    updateaseg_node = Node(UpdateAseg(), name='updateaseg_node')
    updateaseg_node.inputs.subjects_dir = subjects_dir
    updateaseg_node.inputs.subject_id = subject_id
    updateaseg_node.inputs.paint_cc_file = paint_cc_file
    updateaseg_node.inputs.python_interpret = '/home/anning/miniconda3/envs/3.8/bin/python3'
    # updateaseg_node.inputs.python_interpret = '/home/youjia/anaconda3/envs/3.8/bin/python3'
    updateaseg_node.inputs.seg_file = subject_mri_dir / 'aparc.DKTatlas+aseg.deep.mgz'
    updateaseg_node.inputs.aseg_noCCseg_file = subject_mri_dir / 'aseg.auto_noCCseg.mgz'
    updateaseg_node.inputs.aseg_auto_file = subject_mri_dir / 'aseg.auto.mgz'
    updateaseg_node.inputs.cc_up_file = subject_mri_dir / 'transforms' / 'cc_up.lta'
    updateaseg_node.inputs.aparc_aseg_file = subject_mri_dir / 'aparc.DKTatlas+aseg.deep.withCC.mgz'
    updateaseg_node.run()


def SampleSegmentationToSurfave_test():
    subjects_dir = Path("/mnt/ngshare/DeepPrep_flowtest/V001/derivatives/deepprep/Recon")
    subject_id = "sub-002"

    subjects_dir = Path('/mnt/ngshare/Data_Mirror/pipeline_test')
    subject_id = 'sub-MSC01'

    subject_mri_dir = subjects_dir / subject_id / 'mri'
    subject_surf_dir = subjects_dir / subject_id / 'surf'
    subject_label_dir = subjects_dir / subject_id / 'label'
    os.environ['SUBJECTS_DIR'] = str(subjects_dir)

    SampleSegmentationToSurfave_node = Node(SampleSegmentationToSurfave(), name='SampleSegmentationToSurfave_node')
    SampleSegmentationToSurfave_node.inputs.subjects_dir = subjects_dir
    SampleSegmentationToSurfave_node.inputs.subject_id = subject_id
    # SampleSegmentationToSurfave_node.inputs.python_interpret = Path('/home/youjia/anaconda3/envs/3.8/bin/python3')
    SampleSegmentationToSurfave_node.inputs.python_interpret = Path('/home/anning/miniconda3/envs/3.8/bin/python3')
    SampleSegmentationToSurfave_node.inputs.freesurfer_home = Path('/usr/local/freesurfer')
    # SampleSegmentationToSurfave_node.inputs.aparc_aseg_file = subject_mri_dir / 'aparc.DKTatlas+aseg.deep.withCC.mgz'
    SampleSegmentationToSurfave_node.inputs.aparc_aseg_file = subject_mri_dir / 'aparc.DKTatlas+aseg.deep.withCC.mgz'
    # SampleSegmentationToSurfave_node.inputs.aparc_aseg_file = subject_mri_dir / 'aseg.auto.mgz'
    smooth_aparc_file = Path.cwd().parent / 'FastSurfer' / 'recon_surf' / 'smooth_aparc.py'
    SampleSegmentationToSurfave_node.inputs.smooth_aparc_file = smooth_aparc_file

    lh_DKTatlaslookup_file = Path.cwd().parent / 'FastSurfer' / 'recon_surf' / f'lh.DKTatlaslookup.txt'
    rh_DKTatlaslookup_file = Path.cwd().parent / 'FastSurfer' / 'recon_surf' / f'rh.DKTatlaslookup.txt'
    SampleSegmentationToSurfave_node.inputs.lh_DKTatlaslookup_file = lh_DKTatlaslookup_file
    SampleSegmentationToSurfave_node.inputs.rh_DKTatlaslookup_file = rh_DKTatlaslookup_file
    SampleSegmentationToSurfave_node.inputs.lh_white_preaparc_file = subject_surf_dir / f'lh.white.preaparc'
    SampleSegmentationToSurfave_node.inputs.rh_white_preaparc_file = subject_surf_dir / f'rh.white.preaparc'
    lh_aparc_DKTatlas_mapped_prefix_file = subject_label_dir / f'lh.aparc.DKTatlas.mapped.prefix.annot'
    rh_aparc_DKTatlas_mapped_prefix_file = subject_label_dir / f'rh.aparc.DKTatlas.mapped.prefix.annot'
    SampleSegmentationToSurfave_node.inputs.lh_aparc_DKTatlas_mapped_prefix_file = lh_aparc_DKTatlas_mapped_prefix_file
    SampleSegmentationToSurfave_node.inputs.rh_aparc_DKTatlas_mapped_prefix_file = rh_aparc_DKTatlas_mapped_prefix_file
    SampleSegmentationToSurfave_node.inputs.lh_cortex_label_file = subject_label_dir / f'lh.cortex.label'
    SampleSegmentationToSurfave_node.inputs.rh_cortex_label_file = subject_label_dir / f'rh.cortex.label'
    lh_aparc_DKTatlas_mapped_file = subject_label_dir / f'lh.aparc.DKTatlas.mapped.annot'
    rh_aparc_DKTatlas_mapped_file = subject_label_dir / f'rh.aparc.DKTatlas.mapped.annot'
    SampleSegmentationToSurfave_node.inputs.lh_aparc_DKTatlas_mapped_file = lh_aparc_DKTatlas_mapped_file
    SampleSegmentationToSurfave_node.inputs.rh_aparc_DKTatlas_mapped_file = rh_aparc_DKTatlas_mapped_file
    SampleSegmentationToSurfave_node.run()


if __name__ == '__main__':
    set_envrion()

    # Segment_test()

    # Noccseg_test()

    # N4_bias_correct_test()

    # talairach_and_nu_test()

    UpdateAseg_test()

    # SampleSegmentationToSurfave_test()