"""Serialize observed P3 setup/download evidence; never imports a detector."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
YW = '/home/wenchang/asdasdsad/wjq/TOVD/shared/t013_yoloworld'
url = 'https://huggingface.co/wondervictor/YOLO-World-V2.1/resolve/c620164ee3979bf49b895c8a8e0f49aeaca89209/s_stage2-4466ab94.pth'
failure = (OUT/'checkpoint_download.log').read_text().splitlines()[-1]
versions = {name: None for name in ['torch','torchvision','numpy','mmengine','mmcv','mmdet','transformers','timm','opencv-python-headless']}
receipt = {
    'task': 'T013-YW-P3',
    'task_start_head': '2789d06ae8496ed624b91a5f048aa50b288a8776',
    'lead_instruction_commit': '501d8b2ce57b82366e3ee2095aabe3eee0391413',
    'state': 'YW_P3_BLOCKER_RETURN_TO_LEAD',
    'started_at': '2026-09-14T13:11:42+08:00',
    'stopped_at': (OUT/'stopped_at.txt').read_text().strip(),
    'first_blocker': {'phase': 'authorized checkpoint download', 'exit_code': 28, 'exact_message': failure},
    'environment': {'path': YW+'/env', 'python': '3.10.12', 'cuda_compiler': '11.8.89',
        'cuda_compiler_path': '/home/wenchang/anaconda3/envs/lqt_canconv_cu118/bin/nvcc',
        'gpu_target': 'A6000 / cuda:1', 'gpu_runtime_verified_in_p3': False,
        'package_versions': versions, 'installed_distributions': json.loads((OUT/'environment_packages.json').read_text()),
        'source_build_occurred': False},
    'sources': json.loads((OUT/'source_receipt.json').read_text()),
    'checkpoint': {'url': url, 'path': YW+'/weights/s_stage2-4466ab94.pth',
        'expected_bytes':305058902, 'expected_sha256':'4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458',
        'file_exists':False, 'actual_bytes':None, 'actual_sha256':None,
        'other_checkpoint_model_downloaded':False},
    'existing_text_cache': {'action':'copied existing local cache; no network model download',
        'source':'/home/liujianhua/.cache/huggingface/hub/models--openai--clip-vit-base-patch32',
        'destination':YW+'/cache/huggingface/hub/models--openai--clip-vit-base-patch32',
        'snapshot':'3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268',
        'weight_sha256':'a63082132ba4f97a80bea76823f544493bffa8082296d62d71581a4feff1576f'},
    'commands': [
        {'command':f'/usr/bin/python3.10 -m venv {YW}/env', 'exit_code':0},
        {'command':f'{YW}/env/bin/python -m pip --cache-dir {YW}/cache install torch==2.1.2+cu118 torchvision==0.16.2+cu118 numpy==1.26.4 --extra-index-url https://download.pytorch.org/whl/cu118',
         'exit_code':143,'reason':'explicit SIGTERM after checkpoint blocker; not a Torch dependency failure',
         'partial_torch_wheel_bytes':int((OUT/'torch_partial_bytes.txt').read_text())},
        {'command':f'curl -fL --max-time 900 --output {YW}/weights/s_stage2-4466ab94.pth "{url}"', 'exit_code':28},
        {'command':'kill -TERM 1227040', 'exit_code':0, 'pid_command_verified_before_signal':True,
         'process_absent_confirmed_at':'2026-09-14T13:32:26+08:00'},
        {'command':f'{YW}/env/bin/python -m pip list --format=json', 'exit_code':0},
        {'command':'mmcv build / CUDA-op import / model load / synthetic_smoke.py', 'exit_code':None,'status':'NOT_RUN'}],
    'mmcv_wheel_probe': {'index':'https://download.openmmlab.com/mmcv/dist/cu118/torch2.1.0/index.html',
        'matching_mmcv_2_0_0_wheel_found':False,'source_build_started':False},
    'synthetic_image': json.loads((OUT/'synthetic_receipt.json').read_text()),
    'cuda_op_check':'NOT_RUN', 'model_load':'NOT_RUN',
    'vocabularies': [{'name':name,'semantic_count':count,'runtime_count':count+1,'blank_index':count,
        'model_accepted_class_count':None,'native_retained_count':None,'blank_retained_count':None,
        'post_blank_removal_count':None,'nan_inf_check':'NOT_RUN','forward_count':0}
        for name,count in [('V0',80),('Vhard30',110),('Vrand30',110)]],
    'peak_cuda_allocated_bytes':None,'peak_lte_24_gib':None,
    'source_patch_count':0,'alternative_version_checkpoint_model_attempts':0,
    'scientific_actions': {key:0 for key in ['T013_selected_images','T013_corruptions','COCO_LVIS_annotations_or_evaluation',
        'scientific_metrics_or_gates','Grounding_rerun','T014','CF_MECH_scientific_work','YOLO_scientific_benchmark']},
    'remaining_running_p3_processes':0,
    'prepared_smoke_driver_executed':False,
    'next_action':'Research Lead blocker review',
    'preflight_notes':['The conventional /usr/local/cuda-11.8/bin/nvcc path is absent; existing exact 11.8.89 compiler found without modification.',
        'Optional missing-directory listing and cache-search no-match exits were preflight observations, not fixed-lane failures.'],
}
(OUT/'p3_receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
report = f'''# T013-YW-P3 — runtime setup blocked

State: **YW_P3_BLOCKER_RETURN_TO_LEAD**. Started {receipt['started_at']}; stopped {receipt['stopped_at']}.
Task-start HEAD: `{receipt['task_start_head']}`. Lead instruction: `{receipt['lead_instruction_commit']}`.

First exact blocker (checkpoint curl exit 28):
```
{failure}
```
The authorized checkpoint file was not created; actual size/hash are unavailable. No model was downloaded. Torch download had received 287928320 bytes and was explicitly stopped with SIGTERM after this blocker (exit 143); this is not evidence of Torch incompatibility. No P3 process remains running. No alternate transport/model/version attempt or source patch followed the blocker.

Created isolated Python 3.10.12 environment `{YW}/env`; only pip 22.0.2 and setuptools 59.6.0 are installed. All target ML package versions remain unavailable, not verified. Existing CUDA compiler 11.8.89 was located; A6000/cuda:1 was the intended runtime, not tested in P3. No mmcv source build, CUDA-op check, model load or GPU forward ran. The official wheel index had no mmcv 2.0.0 match. No claim of runtime incompatibility or scientific failure follows from this network failure.

Exact preregistered YOLO and MMYOLO revisions were archived and extracted to the isolated source folder, with archive hashes matched remotely (see source_receipt.json). Source-patch count 0. Existing CLIP snapshot was copied into the isolated cache; no extra model download occurred. Synthetic bytes use the required RGB uint8 640×960×3 formula `(13*x+7*y+53*c)%256`, SHA256 `886a1ad7bfca38b1b829d91a0e9f2c15da95a022c67a905675b8552c5cad8592`.

V0 semantic/runtime/blank = 80/81/80; Vhard30 = 110/111/110; Vrand30 = 110/111/110. Every forward count is 0. Accepted class counts, prediction counts, blank-removal counts, finite checks and peak CUDA memory are all NOT RUN / null. The prepared synthetic_smoke.py was not executed and is not validated runtime evidence.

No selected T013 image/corruption, COCO/LVIS annotation/evaluation, scientific metric/gate, Grounding rerun, T014, CF/MECH scientific work, or YOLO scientific benchmark ran. Grounding remains canonically GROUNDING_PRIMARY_NOT_SUPPORTED. No checkpoint/version/model alternative was attempted.

Exact commands, exit codes, sources and expected checkpoint values are in p3_receipt.json; raw download/process logs are adjacent. Changed project paths are this p3 folder, research_log/session_log.md and coordination/CODEX_TO_CHATGPT.md. File hashes are in delivery_manifest.json. Stop after this delivery; an unchanged heartbeat must not retry P3.

Recommended next action: **Research Lead blocker review**.
'''
(OUT/'P3_RUNTIME_REPORT.md').write_text(report,encoding='utf-8')
with (ROOT/'coordination/CODEX_TO_CHATGPT.md').open('a',encoding='utf-8') as f:
    f.write('\n\n---\n\n'+report+'\nFull machine-readable evidence:\n```json\n'+json.dumps(receipt,indent=2,ensure_ascii=False)+'\n```\n')
with (ROOT/'research_log/session_log.md').open('a',encoding='utf-8') as f:
    f.write('\n\n## '+receipt['stopped_at']+' — T013-YW-P3 BLOCKER\n'+
        'Exact authorized checkpoint curl failed exit28 connecting to huggingface.co:443 after134537ms. No file received; no retry/alternative. Stopped only verified P3 pip PID1227040 (exit143, partial287928320 bytes); absent verified13:32:26+08. Python3.10.12 isolated env contains only pip/setuptools. Exact source archives, synthetic bytes and copied existing CLIP cache persisted. No mmcv build/model/GPU/science ran; prepared driver not executed. See research_log/t013_yoloworld/p3/p3_receipt.json and P3_RUNTIME_REPORT.md. State YW_P3_BLOCKER_RETURN_TO_LEAD. Await Research Lead blocker review; no unchanged-mailbox retry.\n')
files = sorted(p for p in OUT.iterdir() if p.is_file() and p.name!='delivery_manifest.json')
files += [ROOT/'coordination/CODEX_TO_CHATGPT.md',ROOT/'research_log/session_log.md']
manifest={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(OUT/'delivery_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(receipt['state'])
