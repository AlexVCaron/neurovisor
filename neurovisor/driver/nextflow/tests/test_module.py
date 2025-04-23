from neurovisor.driver.nextflow.module import (
    Module,
    create_container_command,
    create_input_map,
    create_output_map
)


def test_create_input_map():
    # Test the create_input_map function
    inputs = ["tuple val(meta),path(img)", "path(img2)"]
    expected = {
        0: {
            "type": "neurovisor.model.input.Input",
            "data": None,
            "spec": "tuple val(meta),path(img)"
        },
        1: {
            "type": "neurovisor.model.input.Input",
            "data": None,
            "spec": "path(img2)"
        }
    }
    result = create_input_map(inputs)
    assert result.serialize() == expected, f"Expected {expected}, but got {result}"


def test_create_output_map():
    # Test the create_output_map function
    outputs = ["tuple val(meta),path(img),emit:img", "path(img2),emit:img2,optional:true"]
    expected = {
        "img": {
            "type": "neurovisor.model.output.Output",
            "data": None,
            "spec": "tuple val(meta),path(img)",
            "optional": False
        },
        "img2": {
            "type": "neurovisor.model.output.Output",
            "data": None,
            "spec": "path(img2)",
            "optional": True
        }
    }
    result = create_output_map(outputs)
    assert result.serialize() == expected, f"Expected {expected}, but got {result}"


def test_create_parameters_map():
    pass


def test_create_single_container_command():
    # Test the create_single_container_command function
    script = "echo hello"
    containers = "container_name"
    expected = {
        "command": script,
        "containers": [
            {
                "image": containers,
                "configuration": {}
            }
        ]
    }
    result = create_container_command(script, containers)
    assert result.serialize() == expected, f"Expected {expected}, but got {result}"


def test_create_multiple_container_command():
    # Test the create_multiple_container_command function
    script = "echo hello"
    containers = '{params.docker ? "docker_container" : "apptainer_container"}'
    expected = {
        "command": script,
        "containers": [
            {
                "image": "docker_container",
                "configuration": {}
            },
            {
                "image": "apptainer_container",
                "configuration": {}
            }
        ]
    }
    result = create_container_command(script, containers)
    assert result.serialize() == expected, f"Expected {expected}, but got {result}"


def test_module(shared_datadir):
    # Test the module function
    script = '"""\n    export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=$task.cpus\n    export OMP_NUM_THREADS=$task.cpus\n    export OPENBLAS_NUM_THREADS=1\n    export ANTS_RANDOM_SEED=7468\n    export MRTRIX_RNG_SEED=12345\n\n    orig_bval=$bval\n    # Concatenate DWIs\n    number_rev_dwi=0\n    if [[ -f "$rev_dwi" ]];\n    then\n        scil_dwi_concatenate.py ${prefix}__concatenated_dwi.nii.gz ${prefix}__concatenated_dwi.bval ${prefix}__concatenated_dwi.bvec -f\n            --in_dwis ${dwi} ${rev_dwi} --in_bvals ${bval} ${rev_bval}\n            --in_bvecs ${bvec} ${rev_bvec}\n\n        number_rev_dwi=$(scil_header_print_info.py ${rev_dwi} --key dim | sed "s/  / /g" | sed "s/  / /g" | rev | cut -d\' \' -f4-4 | rev)\n\n        dwi=${prefix}__concatenated_dwi.nii.gz\n        bval=${prefix}__concatenated_dwi.bval\n        bvec=${prefix}__concatenated_dwi.bvec\n    else\n        dwi=${dwi}\n        bval=${bval}\n        bvec=${bvec}\n    fi\n\n    # If topup has been run before\n    if [[ -f "$topup_fieldcoef" ]]\n    then\n        mrconvert $corrected_b0s b0_corrected.nii.gz -coord 3 0 -axes 0,1,2 -nthreads $task.cpus\n        bet b0_corrected.nii.gz ${prefix}__b0_bet.nii.gz -m -R\n            -f $bet_topup_before_eddy_f\n\n        scil_dwi_prepare_eddy_command.py ${dwi} ${bval} ${bvec} ${prefix}__b0_bet_mask.nii.gz\n            --topup $prefix_topup --eddy_cmd $eddy_cmd\n            --b0_thr $b0_thr_extract_b0\n            --encoding_direction $encoding\n            --readout $readout --out_script --fix_seed\n            --n_reverse ${number_rev_dwi}\n            --lsr_resampling\n            $slice_drop_flag\n    else\n        scil_dwi_extract_b0.py ${dwi} ${bval} ${bvec} ${prefix}__b0.nii.gz --mean\n            --b0_threshold $b0_thr_extract_b0 --skip_b0_check\n        bet ${prefix}__b0.nii.gz ${prefix}__b0_bet.nii.gz -m -R -f $bet_prelim_f\n        scil_volume_math.py convert ${prefix}__b0_bet_mask.nii.gz ${prefix}__b0_bet_mask.nii.gz --data_type uint8 -f\n        maskfilter ${prefix}__b0_bet_mask.nii.gz dilate ${prefix}__b0_bet_mask_dilated.nii.gz\n            --npass $dilate_b0_mask_prelim_brain_extraction -nthreads $task.cpus\n        scil_volume_math.py multiplication ${prefix}__b0.nii.gz ${prefix}__b0_bet_mask_dilated.nii.gz\n            ${prefix}__b0_bet.nii.gz --data_type float32 -f\n\n        scil_dwi_prepare_eddy_command.py ${dwi} ${bval} ${bvec} ${prefix}__b0_bet_mask.nii.gz\n            --eddy_cmd $eddy_cmd --b0_thr $b0_thr_extract_b0\n            --encoding_direction $encoding\n            --readout $readout --out_script --fix_seed\n            $slice_drop_flag\n    fi\n\n    echo "--very_verbose $extra_args --nthr=$task.cpus" >> eddy.sh\n    sh eddy.sh\n    scil_volume_math.py lower_clip dwi_eddy_corrected.nii.gz 0 ${prefix}__dwi_corrected.nii.gz\n\n    if [[ $number_rev_dwi -eq 0 ]]\n    then\n        mv dwi_eddy_corrected.eddy_rotated_bvecs ${prefix}__dwi_eddy_corrected.bvec\n        mv ${orig_bval} ${prefix}__dwi_eddy_corrected.bval\n    else\n        scil_gradients_validate_correct_eddy.py dwi_eddy_corrected.eddy_rotated_bvecs ${bval} ${number_rev_dwi} ${prefix}__dwi_eddy_corrected.bvec ${prefix}__dwi_eddy_corrected.bval\n    fi\n\n    if $run_qc;\n    then\n        extract_dim=$(mrinfo ${dwi} -size)\n        read sagittal_dim coronal_dim axial_dim fourth_dim <<< "${extract_dim}"\n\n        # Get the middle slice\n        coronal_dim=$(($coronal_dim / 2))\n        axial_dim=$(($axial_dim / 2))\n        sagittal_dim=$(($sagittal_dim / 2))\n\n        viz_params="--display_slice_number --display_lr --size 256 256"\n        rev_dwi=""\n        if [[ -f "$rev_dwi" ]];\n        then\n            scil_dwi_powder_average.py ${rev_dwi} ${prefix}__dwi_eddy_corrected.bval ${prefix}__rev_dwi_powder_average.nii.gz\n            scil_volume_math.py normalize_max ${prefix}__rev_dwi_powder_average.nii.gz ${prefix}__rev_dwi_powder_average_norm.nii.gz\n            rev_dwi="rev_dwi"\n        fi\n        scil_dwi_powder_average.py ${dwi} ${prefix}__dwi_eddy_corrected.bval ${prefix}__dwi_powder_average.nii.gz\n        scil_dwi_powder_average.py ${prefix}__dwi_corrected.nii.gz ${prefix}__dwi_eddy_corrected.bval ${prefix}__dwi_corrected_powder_average.nii.gz\n        scil_volume_math.py normalize_max ${prefix}__dwi_powder_average.nii.gz ${prefix}__dwi_powder_average_norm.nii.gz\n        scil_volume_math.py normalize_max ${prefix}__dwi_corrected_powder_average.nii.gz ${prefix}__dwi_corrected_powder_average_norm.nii.gz\n\n        for image in dwi_corrected dwi ${rev_dwi}\n        do\n            scil_viz_volume_screenshot.py ${prefix}__${image}_powder_average_norm.nii.gz ${prefix}__${image}_coronal.png ${viz_params} --slices ${coronal_dim} --axis coronal\n            scil_viz_volume_screenshot.py ${prefix}__${image}_powder_average_norm.nii.gz ${prefix}__${image}_axial.png ${viz_params} --slices ${axial_dim} --axis axial\n            scil_viz_volume_screenshot.py ${prefix}__${image}_powder_average_norm.nii.gz ${prefix}__${image}_sagittal.png ${viz_params} --slices ${sagittal_dim} --axis sagittal\n\n            if [ $image == "dwi_corrected" ] || [ $image == "rev_dwi" ]\n            then\n                title="After"\n            else\n                title="Before"\n            fi\n\n            convert +append ${prefix}__${image}_coronal_slice_${coronal_dim}.png \n                    ${prefix}__${image}_axial_slice_${axial_dim}.png  \n                    ${prefix}__${image}_sagittal_slice_${sagittal_dim}.png \n                    ${prefix}__${image}.png\n\n            convert -annotate +20+230 "${title}" -fill white -pointsize 30 ${prefix}__${image}.png ${prefix}__${image}.png\n        done\n\n        if [[ -f "$rev_dwi" ]];\n        then\n            convert -delay 10 -loop 0 -morph 10 \n                ${prefix}__rev_dwi.png ${prefix}__dwi_corrected.png ${prefix}__rev_dwi.png \n                ${prefix}__rev_dwi_eddy_mqc.gif\n        fi\n\n        convert -delay 10 -loop 0 -morph 10 \n                ${prefix}__dwi.png ${prefix}__dwi_corrected.png ${prefix}__dwi.png \n                ${prefix}__dwi_eddy_mqc.gif\n\n        rm -rf *png\n        rm -rf *powder_average*\n    fi\n\n    cat <<-END_VERSIONS > versions.yml\n    "${task.process}":\n        scilpy: $(pip list | grep scilpy | tr -s \' \' | cut -d\' \' -f2)\n        mrtrix: $(dwidenoise -version 2>&1 | sed -n \'s/== dwidenoise \\([0-9.]\\+\\).*/\\1/p\')\n        fsl: $(flirt -version 2>&1 | sed -n \'s/FLIRT version \\([0-9.]\\+\\)/\\1/p\')\n        imagemagick: $(convert -version | sed -n \'s/.*ImageMagick \\([0-9]\\{1,\\}\\.[0-9]\\{1,\\}\\.[0-9]\\{1,\\}\\).*/\\1/p\')\n    END_VERSIONS\n    """'

    expected = {
        "command": {
            "command": script,
            "containers": [
                {
                    "image": "scilus/scilus:latest",
                    "configuration": {}
                },
                {
                    "image": "https://scil.usherbrooke.ca/containers/scilus_latest.sif",
                    "configuration": {}
                }
            ]
        },
        "parameters": {},
        "inputs": {
            0: {
                "type": "neurovisor.model.input.Input",
                "data": None,
                "spec": "tuple val(meta),path(dwi),path(bval),path(bvec),path(rev_dwi),path(rev_bval),path(rev_bvec),path(corrected_b0s),path(topup_fieldcoef),path(topup_movpart)"
            }
        },
        "outputs": {
            "dwi_corrected": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__dwi_corrected.nii.gz")',
                "optional": False
            },
            "bval_corrected": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__dwi_eddy_corrected.bval")',
                "optional": False
            },
            "bvec_corrected": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__dwi_eddy_corrected.bvec")',
                "optional": False
            },
            "b0_mask": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__b0_bet_mask.nii.gz")',
                "optional": False
            },
            "dwi_eddy_mqc": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__dwi_eddy_mqc.gif")',
                "optional": True
            },
            "rev_dwi_eddy_mqc": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'tuple val(meta),path("*__rev_dwi_eddy_mqc.gif")',
                "optional": True
            },
            "versions": {
                "type": "neurovisor.model.output.Output",
                "data": None,
                "spec": 'path("versions.yml")',
                "optional": False
            }

        }
    }

    module = Module(f"{shared_datadir}/module/preproc/eddy")
    result = module.serialize()
    assert result == expected, f"Expected {expected}, but got {result}"