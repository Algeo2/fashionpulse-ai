from pathlib import Path
import hashlib
import json
import urllib.request
import zipfile
import streamlit as st

@st.cache_resource(show_spinner=False)
def ensure_runtime():
    root=Path(__file__).resolve().parent
    archive=root/'runtime.zip'
    expected=(root/'archive_sha256.txt').read_text().strip()
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:
        raise RuntimeError('Runtime archive checksum mismatch')
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            if not (root/name).resolve().is_relative_to(root):
                raise RuntimeError('Invalid archive path')
        z.extractall(root)
    origin=root/'bundle/outputs/visuelle_embeddings'
    info=json.loads((origin/'encoder.json').read_text())
    weights=origin/info['weights'].replace('\\','/')
    expected=info['weights_sha256']
    if not weights.exists() or hashlib.sha256(weights.read_bytes()).hexdigest()!=expected:
        url='https://huggingface.co/timm/resnet18.a1_in1k/resolve/491b427b45c94c7fb0e78b5474cc919aff584bbf/model.safetensors'
        weights.parent.mkdir(parents=True,exist_ok=True)
        temporary=weights.with_suffix('.download')
        digest=hashlib.sha256()
        with urllib.request.urlopen(url,timeout=120) as response, temporary.open('wb') as target:
            while chunk:=response.read(1024*1024):
                digest.update(chunk)
                target.write(chunk)
        if digest.hexdigest()!=expected:
            raise RuntimeError('Encoder checksum mismatch')
        temporary.replace(weights)
    return True
