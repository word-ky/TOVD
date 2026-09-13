# MECH1 static command receipt

Local PowerShell used existing Autodl.Common.ps1, project .autodl/config.json,
Invoke-AutodlSsh and Copy-FromAutodl. No model command executed.

```powershell
$env:AUTODL_CONFIG_PATH='D:\work\fightccfa-agin\CVPR2027\TTT-OVD\.autodl\config.json'
. ./scripts/Autodl.Common.ps1
```

Exact remote source metadata/hash commands:

```bash
stat -c %s /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/native_source.tar.gz
cd /home/wenchang/asdasdsad/wjq/TOVD/shared/t013/native && sha256sum groundingdino/config/GroundingDINO_SwinT_OGC.py groundingdino/models/GroundingDINO/groundingdino.py groundingdino/models/GroundingDINO/transformer.py groundingdino/models/GroundingDINO/fuse_modules.py groundingdino/models/GroundingDINO/bertwarper.py groundingdino/models/GroundingDINO/utils.py groundingdino/models/GroundingDINO/transformer_vanilla.py
```

Copy-FromAutodl source=/home/wenchang/asdasdsad/wjq/TOVD/shared/t013/native_source.tar.gz,
destination=D:/work/fightccfa-agin/CVPR2027/TTT-OVD/research_log/t013/mech1/native_source.tar.gz.
Local static Python3.12.7 command: PowerShell here-string piped to
D:/anaconda3/python.exe -. Used hashlib.sha256(path.read_bytes()),
tarfile.open(...).extractfile(name).read() for the exact seven names above,
and equality against parsed remote_source_sha256.txt. No extractall,
module import, checkpoint load, model command or dataset read.

Exact Git source commands:

```text
git show 6fec32243985ccc808123d851abf5f3dea10af99:scripts/t013_native_detector.py
git show 6fec32243985ccc808123d851abf5f3dea10af99:scripts/t013_native_run.py
git show 6fec32243985ccc808123d851abf5f3dea10af99:scripts/t013_text.py
```

Source text inspected using rg -n for def/text_dict/topk/tgt_embed/refpoint/
two_stage/enc_outputs/hs/outputs_class/outputs_coord/bert/feat_map/transformer,
and bounded numbered Python text reads. Trace line ranges are listed in
MECHANISM_IDENTIFIABILITY_AUDIT.md. No AST/runtime execution of native code.

The already-authorized primary scalar health command ran once before the
concurrent Lead update, with the exact timestamp/scalars retained in the
machine receipt. No active-primary scientific files or annotations read.
