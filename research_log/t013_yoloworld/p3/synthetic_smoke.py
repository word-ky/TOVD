"""P3 only: pinned native online-text inference on one synthetic image; no metrics."""
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import sys
import traceback

ROOT = Path('/home/wenchang/asdasdsad/wjq/TOVD')
YW = ROOT/'shared/t013_yoloworld'
OUT = YW/'p3'
SOURCE = YW/'source'
CONFIG = 'configs/pretrain/yolo_world_v2_s_vlpan_bn_2e-3_100e_4x8gpus_obj365v1_goldg_train_1280ft_lvis_minival.py'
sys.path[:0] = [str(SOURCE), str(SOURCE/'third_party/mmyolo'), str(OUT)]

def main():
    receipt={'task':'T013-YW-P3','status':'RUNNING','vocabularies':[],
             'scientific_image_or_annotations_used':False,'scientific_metrics_computed':False,
             'source_patch_count':0,'alternative_model_or_version_attempts':0}
    try:
        import numpy as np
        import torch
        expected={'torch':'2.1.2+cu118','torchvision':'0.16.2+cu118','numpy':'1.26.4',
                  'mmengine':'0.10.3','mmdet':'3.0.0','mmcv':'2.0.0','transformers':'4.36.2',
                  'timm':'0.6.13','opencv-python-headless':'4.9.0.80'}
        receipt['versions']={k:metadata.version(k) for k in expected}
        assert receipt['versions']==expected, 'fixed package lane mismatch'
        installed={d.metadata['Name'].lower() for d in metadata.distributions()}
        assert not {'mmcv-lite','opencv-python','opencv-contrib-python','opencv-contrib-python-headless'} & installed
        assert sys.version_info[:2]==(3,10) and torch.version.cuda=='11.8'
        device='cuda:1'
        receipt['device']=device
        receipt['gpu']=torch.cuda.get_device_name(device)
        assert 'A6000' in receipt['gpu']
        from mmcv.ops import nms
        boxes=torch.tensor([[0.,0.,10.,10.],[1.,1.,9.,9.]],device=device)
        scores=torch.tensor([.9,.8],device=device)
        _, indices=nms(boxes,scores,.7)
        receipt['cuda_nms']={'executed':True,'output_count':len(indices),'finite':True}
        from mmengine.config import Config
        from mmengine.dataset import Compose
        from mmengine.runner import load_checkpoint
        from mmdet.apis import init_detector
        from protocol_adapter import runtime_texts, semantic_predictions
        checkpoint=YW/'weights/s_stage2-4466ab94.pth'
        ckpt_bytes=checkpoint.read_bytes()
        receipt['checkpoint']={'path':str(checkpoint),'bytes':len(ckpt_bytes),'sha256':hashlib.sha256(ckpt_bytes).hexdigest()}
        assert len(ckpt_bytes)==305058902 and receipt['checkpoint']['sha256']=='4466ab940ab2d93ff436b4869961bb885d7faf176bd0c8511d3cf451af55f458'
        del ckpt_bytes
        cfg=Config.fromfile(str(SOURCE/CONFIG))
        torch.cuda.reset_peak_memory_stats(device)
        model=init_detector(cfg,checkpoint=None,device=device)
        # Standard framework loading, strict state-key consistency. No patches.
        load_checkpoint(model,str(checkpoint),map_location='cpu',strict=True)
        model.eval().float()
        receipt['checkpoint_load']='standard mmengine load_checkpoint strict=True PASS'
        native=dict(model.bbox_head.test_cfg)
        for key,value in {'multi_label':True,'score_thr':.001,'nms_pre':30000,'max_per_img':300}.items():
            assert native[key]==value, 'native postprocessing mismatch: '+key
        assert native['nms']['iou_threshold']==.7 and native['nms']['type']=='nms'
        receipt['native_postprocessing']=native
        # Standard in-memory input loading; annotations are irrelevant to predict.
        # Keep resize/letterbox/LoadText/PackDetInputs from the selected config.
        pipeline_cfg=[dict(item) for item in cfg.test_pipeline if item['type']!='LoadAnnotations']
        pipeline_cfg[0]['type']='mmdet.LoadImageFromNDArray'
        pipeline=Compose(pipeline_cfg)
        raw=(OUT/'synthetic_rgb.uint8').read_bytes()
        assert hashlib.sha256(raw).hexdigest()=='886a1ad7bfca38b1b829d91a0e9f2c15da95a022c67a905675b8552c5cad8592'
        rgb=np.frombuffer(raw,dtype=np.uint8).reshape(640,960,3)
        vocab=json.loads((OUT/'vocabulary_native30.json').read_text())['vocabularies']
        for name in ['V0','Vhard30','Vrand30']:
            names=vocab[name]; texts=runtime_texts(names)
            data=pipeline(dict(img_id=0,img_path='synthetic_rgb.uint8',img=rgb[:,:,::-1].copy(),texts=[[t] for t in texts]))
            batch=dict(inputs=data['inputs'].unsqueeze(0),data_samples=[data['data_samples']])
            with torch.inference_mode():
                output=model.test_step(batch)[0]
            torch.cuda.synchronize(device)
            pred=output.pred_instances
            finite=all(bool(torch.isfinite(t).all()) for t in [pred.bboxes,pred.scores,pred.labels])
            rows=[{'label':int(label)} for label in pred.labels.cpu().tolist()]
            kept,blank=semantic_predictions(rows,len(names))
            record={'vocabulary':name,'semantic_count':len(names),'runtime_count':len(texts),'blank_index':len(names),
                    'model_accepted_class_count':model.bbox_head.num_classes,'native_retained_count':len(pred),
                    'blank_retained_count':blank,'post_blank_removal_count':len(kept),'all_finite':finite}
            receipt['vocabularies'].append(record)
            assert len(texts)==(81 if name=='V0' else 111) and model.bbox_head.num_classes==len(texts)
            assert len(pred)<=300 and finite
        receipt['peak_cuda_allocated_bytes']=torch.cuda.max_memory_allocated(device)
        assert receipt['peak_cuda_allocated_bytes']<=24*1024**3
        receipt['status']='YW_P3_RUNTIME_FEASIBILITY_PASS_READY_FOR_LEAD'
    except Exception as exc:
        receipt['status']='YW_P3_BLOCKER_RETURN_TO_LEAD'
        receipt['failure']={'type':type(exc).__name__,'detail':str(exc),'traceback':traceback.format_exc()}
    (OUT/'smoke_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    return 0 if receipt['status']=='YW_P3_RUNTIME_FEASIBILITY_PASS_READY_FOR_LEAD' else 1

if __name__=='__main__':
    raise SystemExit(main())
