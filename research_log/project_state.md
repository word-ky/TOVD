# TOVD project state

T013 ACTIVE — real-detector prerequisites; background COCO download. Scope c07ce16/afe9c13. Latestimplementation1d3f12b; allT001-T012 remainCLOSED.

ACTIVE DATA RUN: 20260912-190511-tovd-t013-coco-ranges-a6000 (release20260912-190401-tovd-t013-coco-ranges), 8HTTP ranges fromofficialCOCOhost, annotationsfirst, then5000valimages. Do notlaunchduplicatewriter. shared/t013/coco retainsrangechunksforcontinuation. Onceannotationsready, select/commit exactly1000IDs withscripts/t013_select_images.py beforeprimary.

TEXT FINAL: 20260912-190708-tovd-t013-text-r3-a6000 exit0 at19:07:40+08,release20260912-190653-tovd-t013-text-final.1124eligible/79excluded; V0/Vhard/Vrand195/408/545tokens. AllfullpromptsencodewithouttruncationusingexistingBERTsentencepositions. ModelstateSHAedb3ae75e8e8d40a61f147eccdfcb5db6a51e4030302d9b8faa8a7db72da7b57 unchanged. Use r3 finalvocabulary; r2 was supersededaftertext-only aliasaudit.

OfficialHFcheckpoint a2bb814d SHA1a2412ef99bd74bcd3c2a246fa1e48581f8889a1300c9051974741314fc042f3 verified, modelreadyinshared/t013/model. Isolatedenvironment shared/t013/venv withTorch2.4.0+cu121,torchvision0.19.0+cu121,Transformers4.44.2,pytest9.1.1. Originalvenv unchanged. Shared1024textcapacity repairsnative256limitwithoutlearnedweightchanges; originalV0detectorparity stillneedsrealsmoke.

No primaryimageinference, no AP/CI/gateoutcomes. FullPLAN/IDs/imagehashes/smoke/cache-runner/COCOmetrics/bootstrap/reportremainpending. Recoverydetails: research_log/t013/IMPLEMENTATION_NEXT.md, PREREQUISITES.md, recentsessionlog. Local/A6000 textunit3passed; prior108synthetictests notrerunforthisphase.

Heartbeat15min ACTIVE andauthorizedtocontinueT013automatically. WaitLeadreviewonlyafterT013scientificreport; do notautonomouslyimplementT014. Updated 2026-09-12T19:09:50.478874+08:00
