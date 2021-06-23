import logging
import re
from antx import transfer
from pathlib import Path

def preprocessing_pudrak(vol_text):
    vol_text = re.sub(r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\]).+", "\g<1>", vol_text )
    return vol_text

def  rm_annotations(text, annotations):
    clean_text = text
    for ann in annotations:
        clean_text = re.sub(ann, '', clean_text)
    return clean_text

def transfer_pg_br(derge_hfml, pudrak_hfml):
    derge_pudrak_text = ""
    anns = [r"\n", r"\[\w+\.\d+\]", r"\[[𰵀-󴉱]?[0-9]+[a-z]{1}\]", r"\{([𰵀-󴉱])?\w+\}",  r"\{([𰵀-󴉱])?\w+\-\w+\}"]
    derge_hfml = rm_annotations(derge_hfml, anns)
    derge_pudrak_text = transfer(
        pudrak_hfml,
        [["linebreak", r"(\n)"], 
        ["pg_ann", r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])"],
        ["double_tseg",r"(:)"],
        ],
        derge_hfml,
        output="txt",
    )
    return derge_pudrak_text


if __name__ == "__main__":
    derge_hfml_paths = list(Path('./derge_vol').iterdir())
    derge_hfml_paths.sort()
    pudrak_hfml_paths = list(Path('./pudrak_trans').iterdir())
    pudrak_hfml_paths.sort()
    for derge_hfml_path, pudrak_hfml_path in zip(derge_hfml_paths, pudrak_hfml_paths):
        print(f'INFO: {pudrak_hfml_path.stem} tranfering line break to {derge_hfml_path.stem}..')
        derge_hfml = derge_hfml_path.read_text(encoding='utf-8')
        pudrak_hfml = pudrak_hfml_path.read_text(encoding='utf-8')
        pudrak_hfml = preprocessing_pudrak(pudrak_hfml)
        derge_pudrak_hfml = transfer_pg_br(derge_hfml, pudrak_hfml)
        Path(f'./derge_pudrak/{pudrak_hfml_path.stem}.txt').write_text(derge_pudrak_hfml, encoding='utf-8')
        print(f'INFO: {pudrak_hfml_path.stem} completed..')

