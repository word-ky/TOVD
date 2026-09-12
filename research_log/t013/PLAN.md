# T013-NATIVE30 preregistration

Status: FINAL PRE-PRIMARY FREEZE. All prerequisites below have passed; this PLAN, native30_freeze.json, code, data hashes, vocabulary, IDs and smoke receipts are committed together before primary execution. Use the exact enclosing main commit as --freeze-commit. Supersedes HF1024/80-distractor primary design under Lead02ba123/259217c. Scientific premise and numerical Gates1–4 unchanged; T001–T012 remain closed. No scientific primary outcomes have been generated.

## Detector and execution

Official native GroundingDINO Swin-T source856dde20aee659246248e20734ef9ba5214f5e44, source archiveSHA8a0270b0ed22391b25fba9c1ddb32cd990c33a3321d26cbc0d9d3a07995fa214. Official native checkpoint ShilongLiu/GroundingDINO revisiona94c9b567a2a374598f05c584e96798a170c56fb, groundingdino_swint_ogc.pth,693997677bytes,SHA3b3ca2563c77c69f651d7bd133e97139c186df06231157a64c507099c52bc799. GroundingDINO_SwinT_OGC.py config, native256textcapacity. Complete checkpoint loaded with no missing keys. No HF detector is loaded for this audit. Native BERT constructor uses the existing local tokenizer/config directory; all learned weights are filled by the complete native checkpoint.

Use CPU FP32, fourTorch/OMP/MKLthreads, eval/inference_mode, gradientsdisabled, native unmodifiedPyTorch deformableattention path. OriginalTorch2.4.0+cu121/torchvision0.19.0+cu121/Transformers4.44.2/NumPy1.26.4. NoAMP, noCUDAkernelcompilation, noimagefeature caching betweenconditions. NoTTT/gradients/weightupdates. Record complete environment and statehashbefore/after. Expectednative stateSHAde1683cc0a3c35157ed5475169dae013cdaffe69f45651d6e3f5550ae96139e1.

Official preprocessing exactly RandomResize([800],max_size=1333),ToTensor,Normalize(mean[.485,.456,.406],std[.229,.224,.225]); noHFprocessor. Both inference and directV0smoke use native transform. CPU runtime may require a long background job; do not change detector numerics for speed after freeze.

## Images, corruptions and vocabularies

COCO2017val sourceofficial images.cocodataset.org archives. AnnotationJSONSHAe8c7f7908f1d7278341fae127d0da654f102f11bd7b21d8aeefa635b8c810b6f. Exactly1000primaryIDs fixed42daa6e, selectionSHA8039a70f25c34f295345e63d1980f692631b6bbdaa5c37267a10852acbf3833b. Selection random.Random(20260912).sample(sorted5000IDs,1000), then sort. Never resample using labels/outcomes. Disjointsmoke139/285/632. Final archiveCRC/SHAreceipt and SHA256ofall5000JPEGs must accompany finalfreeze.

Vocabulary_native30.jsonSHA3bb4a0ebada1f9da407ae6a94f1135798dba7117bd658a6ecba97b2ebfad0967. CanonicalCOCO80names/prefixunchanged. Vhard30 exact2-token subsequence ofacceptedhard80 inoriginalorder; Vrand30 lowestfrozen maxCOCOcosine amongeligible2-token candidates excludinghard30, tiesascendingLVISid. No re-embedding/re-filtering/outcomeselection. Counts80/110/110, tokens195/255/255, histogram2:30both. TokenizerSHA d241a60d5e8f04cc1b2b3e9ef7a4921b27bf526d9f6050ab90f9267a1f9e5c66. Fullstrings,IDs,names,scores andcontributionsincommittedvocabulary. Native actual encoded/masklength195/255/255must passsmoke; no truncation/chunking.

Fiveconditionsinorder clean,gaussian_noise,motion_blur,fog,jpeg_compression; allcorruptionsseverity3 viaimagecorruptions1.1.2, Pillow10.4.0/scikit-image0.24.0/OpenCV4.10.0.84. PixelinputRGBuint8 atoriginalresolution. Beforeeachcorruption resetNumPyseed to(20260912+image_id*17+condition_index*1000003) modulo2**32, cleanindex0. Samegeneratedpixels reused acrossV0,Vhard30,Vrand30; recordpixelSHA256percell. No detector outcome controls corruption or vocabulary.

## Predictions and metrics

scripts/t013_native_run.py reads onlyfrozenIDs/images/vocabulary, neverannotations. Iterate1000IDs, thenfiveconditions, thenV0/Vhard30/Vrand30. Saveall900boxes (pixelxyxy andnormalizedcxcywh), validtokenlogits, canonical/distractorclassscores, top300queryIDs/classes/scores inNPZ. Perclassscore=mean(sigmoidtokenlogits overclassphrase tokens), denominatorcount+1e-6; GEMMonlyvalidtokenlength. Top300fromflattenedquery/classscoresusingtorch.topk. NoAPscorethreshold/NMS/clipping/condition-specificsetting. Keepall15cells evenif earlyoutcomeswouldfailgate; noinspectionortuningduringrun. RecordrawSHA, sourceimageSHA, pixelSHA, immutablecode/configfreezecommitand modelstate.

Mapfirst80classindices toascendingofficialCOCOcategoryIDs. Discarddistractorlabels onlyfromcanonicalAPevaluation, afterglobaltop300selection. Officialpycocotools2.0.8bboxCOCOeval, IoU.50:.05:.95,101recallpoints,areaall,maxDet100perimage/category, sorted1000IDs. AP/mAP50:95 andAP50inpercentagepoints; ARaveragedIoUs andAR50 atmaxDet100alsoinpercentagepoints. Cacheofficialperimage/categoryCOCOmatches atmaxDet300forFPdiagnostics; AP/ARaccumulationuses100. Classesabsentina bootstrap replicate followofficialCOCOignoredprecision-1 convention.

Diagnostics score>=.25andIoU>=.5. CanonicalFP/image usesofficialCOCOmatching/ignore/crowd, up toallselected300; distractorFP/image countsallselecteddistractorlabels (alloutsidecanonicalvocabulary). NoncrowdGTclasscorrectrecall andclassagnosticlocalizationrecall are microobjectcoverage byanyselectedbox, same threshold. Forraw900queries, selectbestIoUquery pernoncrowdGT, GTclassscoreminusmaxdistractorscore ifIoU>=.5. V0hasnomargin. Margincontrast usesonlyGTlocalizedinallfourclean/corrupt×hard/randomcells, identicalGTIDs, so supportdoesnotchangebetweencontrastterms. ReportcommonGTcount.

## Paired image bootstrap and interaction

NumPydefault_rng(20260913), exactly1000replicates, eachsample1000imageindices withreplacement. Savefull1000x1000drawmatrixbeforeaccumulation. Sameindices/draworderacrossall15cellsanddiagnostics. Duplicateimages becomeindependentcopiesofcachedCOCOimage-matches; rerunofficialCOCOeval.accumulate toderivewhole-datasetPRcurve, neveraverageperimageAP. Stabletiedscoresfollowdraworder. TestscomparecachedaccumulationtofullGT/predictionduplication+reevaluation includingcrowd,absentclasses,duplicatesandties. Diagnosticcountsresamplethesameimages, microrecallrecomputedfromsummedcounts. No stratification orclassbalancing.

CI=two-sidedpercentile95%, NumPypercentile[2.5,97.5],methodlinear. D(c,v)=AP50(clean,v)-AP50(c,v). A(c,v)=D(c,v)-D(c,V0). Computecontrastsperreplicate beforeCI. ReportpercorruptionD/A,hard-randomAcontrast,mean4A_hard,mean4hard-random withpairedCIs. AP,AP50,AR,AR50anddiagnostics alsohavepercellCIs. Marginundefinedsupportisreportedunavailable ratherthanimputedzero; do notdiscardundefinedreplicates to fabricate a CI.

## Unchanged scientific gates

Gate1: >=2of4corruptions A_hard>=1.0AP50points and95%CI lower>0. Gate2: mean4A_hard>=.75points, mean4(A_hard-A_rand)>=.50points, >=2positivehard-randompointestimates. Gate4: allsettings frozenbeforeprimary; noresult/labeltuning. Runtimechecksbindcode/vocab/selection/imagehashes andverifysharedpixels/stateimmutability; ResearchLeadalsoauditsGit/protocolhistory.

Gate3 requirescoherentsemanticcompetitionevidence andcannotrescueGates1/2. Prespecifieddiagnostics: (a) corruptionincreaseindistractorFP underhard minusrandom; (b) corruptionincreaseinlocalizationrecall-minusclasscorrectrecallgap underhard minusrandom; (c) clean-to-corruptGTmarginshrinkage underhard minusrandom oncommonlocalizedGTsupport. Positivevalues supportcompetition. Report4pointvalues,meanandpairedCIfor each; implementationprovidesaconservativesupportflag(meanCI lower>0 and>=2positivecorruptions). ThisflagdoesnotreplaceLeadqualitativeGate3decision orchangeGates1/2/4. Noautomaticresearchacceptance.

IfGates1/2/4fail,stopandreportthenative/capacity-saferesult; no vocabredesignorT014. Ifpass,LeadreviewsGate3anddecideswhetheraseparateT014causaltestiswarranted. AllHF/parity/syntheticresultsremainhistoricalengineeringevidenceonly.

## Completed prerequisite receipts

FinalCOCOresume20260912-205852-tovd-coco-resume-final exit0 at20:59:42+08. Valarchive815585330bytes,SHA4f7e2ccb2866ec5041993c9cf2a952bbed69647b115d0f74da7ce8f4bef82f05; allZIPCRCs passed. Exactly5000JPEGhashes inimage_sha256.json, manifestSHA38eb39894b8c0f1924e099b3a1ec0b885fdf7ec43c86933e1dc28186d85c3ba8. AnnotationsarchiveSHA113a836d90195ee1f884e704da6304dfaaecff1f023f49b6ca93c4aaae470268. Preservefailedfirsttransfer190511exit1(ConnectionResetError) andresumereceipt; noprimaryoutcomesduringrepair.

Nativevaliditysmoke20260912-204646-tovd-native30-smoke PASS45cells at20:52:51; masks/textlengths/replay/directV0identity/pixels/weightsallverified. Nativecachedpipeline20260912-205428-tovd-native30-pipeline-smoke PASS45rawcells+10engineeringbootstrapreplicates at20:59:29. ItsrawNPZs47MBremainunderremoteprojectrun; allhashesandrunreceipt/analysisartifactsarearchivedlocally. Theyareengineeringfixtures,notprimarydata. Full17focusedtests passedlocal0.91s andremote0.85s oncurrentcode. Fullknown-answer15cellpipelineunit andduplicate-imageCOCOreevaluation tests included.

Environmentexactpipfreeze in native30_environment.txt. native30_freeze.json contains exactcode/vocab/selection/annotation/image-manifest/PLAN/environment/receipt hashes. Runtimebindssources, selection, vocab, imagebytes, expectednativeinitialstate andannotationbytes; cachemanifestprovesidenticalpixelsacrossvocabulariesandfinalweightsunchanged. Estimated1000imageCPUinference~24.9hours from3-imagepipeline269.109s, plusbootstrapanalysis. Estimateonly; donotalterprotocolforruntime. Remoteavailabledisk31GBbeforearchiveassembly, projectedprimaryraw~15.7GBfrom47MB/3images;largeNPZsremaininremoteprojectrootwithhashmanifest.
