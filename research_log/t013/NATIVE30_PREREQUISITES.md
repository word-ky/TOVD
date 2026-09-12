# T013-NATIVE30 prerequisites progress

Updated 2026-09-12T20:57:37.824880+08:00. Lead02ba123/259217c authorizes native-only30distractor reset. HF1024 rejected; no additional parity attempted. ScientificGates1–4 remainunevaluated.

Vocabularyfreeze eed8d1a: exact hard80 two-token subsequence and matching lowest-similarity random30 from frozen table. Classes80/110/110, tokens195/255/255, SHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967. Candidateembeddings/filter/scores and1000IDs unchanged.

Native45cellsmoke20260912-204646-tovd-native30-smoke (release20260912-204543-tovd-native30-smoke) passed at20:52:51+08,exit0. Three disjointimages139/285/632 ×fivecorruptions×threevocabularies. Actual encodedtext/tokenmask/selfattention-mask lengths195/255/255 verified by native transformerhook. Cleanallvocabreplayexact; V0wrappednormalizedboxes/tokenlogits equalunmodifieddirectnativeforward; pixelreplayindependentofvocabulary; statebefore/afterSHAde1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1. Allparametersfrozen/no gradients. Complete originalreceipt/log/commandrecoveredunderresearch_log/remote_runs.

Officialnativepreprocessing/FP32CPU/fourthreads are fixed inPLAN; GPUkernelpath is not changed to accommodate servercompiler11.8/Torch12.1 mismatch. Deploysmokeextractionpassedbutcurrent-symlinkSSHcalltimedout; verifiedrelease tests14pass, completedonlythefailedsymlinkstep, then dispatchedsingleexplicitrelease run. No duplicateexperiment.

Code d5dc807 implements full15condition rawcache, officialCOCO AP/AP50/AR/AR50, FP/recall/margindiagnostics and1000pairedimagebootstrap. Tests17passlocal2.04s (latest0.91s), remote0.94s. CachedCOCOexactlyequalsfullimage-copyreevaluation, includingcrowd/duplicates/absentclasses/tiedscores; fullsyntheticknown-answer15cellanalysispasses. Annotationsneverenterinference. Native datahash/codebindingsfinalization is pendingfinalfreeze.

Realcachedpipeline run20260912-205428-tovd-native30-pipeline-smoke ACTIVE, release20260912-205335-tovd-native30-pipeline. It runs45cachednonprimarycells and10bootstrapreplicates tovalidateI/O/evaluation. Treat outputs asengineeringfixtures only, neverprimaryscience. Finalreceiptpending.

ExistingCOCOdownload20260912-190511-tovd-t013-coco-ranges-a6000 stillalive; laterparts190–194reached despitecompletionlog169/195. Preservepartialrangefiles; inspectexitbeforeanyresume. FinalCRC/archivehash/5000JPEGhashes pending. Do notstartprimaryuntiltheseplus successfulpipeline andcompletePLAN/native30_freeze.json are committedtogetheronmain. ExistingID/vocabularyhardspecsunchanged.

Filesadded/changed: scripts/t013_native_vocab.py,t013_native_detector.py,t013_native_smoke.py,t013_native_run.py,t013_analysis.py,t013_data_receipt.py; existingt013_coco.pyaddsAR; tests/test_t013_native_vocab.py,test_t013_analysis.py,test_t013_pipeline.py andaffectedCOCOtests; vocabulary_native30.json,PLAN.md,state/logs/receipts. Commands arepreserved inrun.sh; focusedtests python -m pytest tests/test_t013_*.py -q (explicitPowerShellpath expansionlocally). NoAPorinteractionclaim. Nextactionfinishrealcachetest/datareceiptthenfinalfreezeandunchangedprimaryexecution.
