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

def transfer_pg_br(target_hfml, pudrak_hfml):
    target_pudrak_text = ""
    anns = [r"\n", r"\[\w+\.\d+\]", r"\[[𰵀-󴉱]?[0-9]+[a-z]{1}\]", r"\{([𰵀-󴉱])?\w+\}",  r"\{([𰵀-󴉱])?\w+\-\w+\}"]
    target_hfml = rm_annotations(target_hfml, anns)
    target_pudrak_text = transfer(
        pudrak_hfml,
        [["linebreak", r"(\n)"], 
        ["pg_ann", r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])"],
        ["double_tseg",r"(:)"],
        ],
        target_hfml,
        output="txt",
    )
    return target_pudrak_text

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def clean_page(pg_text):
    pg_text = re.sub(r"\[([𰵀-󴉱])?[0-9]+[a-z]{1}\].*","", pg_text)
    pg_text = pg_text.strip()
    return pg_text

def save_pagewise(target_pudrak_hfml, vol_num, target_name):
    vol_path = Path(f'./{target_name}/{vol_num}/').mkdir(parents=True, exist_ok=True)
    pages = get_pages(target_pudrak_hfml)
    for pg_num, page in enumerate(pages, 1):
        pg_text = clean_page(page)
        Path(f'./{target_name}/{vol_num}/{pg_num:04}.txt').write_text(pg_text, encoding="utf-8")


def pipeline(target_paths, source_paths, target_name):
    for target_path, source_path in zip(target_paths[1:], source_paths[1:]):
        print(f'INFO: {source_path.stem} tranfering line break to {target_path.stem}..')
        target_hfml = target_path.read_text(encoding='utf-8')
        source_hfml = source_path.read_text(encoding='utf-8')
        source_hfml = preprocessing_pudrak(source_hfml)
        target_pudrak_hfml = transfer_pg_br(target_hfml, source_hfml)
        save_pagewise(target_pudrak_hfml, target_path.stem, target_name)
        Path(f'./{target_name}_trans_pudrak/{source_path.stem}.txt').write_text(target_pudrak_hfml, encoding='utf-8')
        print(f'INFO: {source_path.stem} completed..')

if __name__ == "__main__":
    # derge_hfml_paths = list(Path('./derge_vol').iterdir())
    # derge_hfml_paths.sort()
    # pudrak_hfml_paths = list(Path('./pudrak_trans').iterdir())
    # pudrak_hfml_paths.sort()
    # for derge_hfml_path, pudrak_hfml_path in zip(derge_hfml_paths, pudrak_hfml_paths):
    #     print(f'INFO: {pudrak_hfml_path.stem} tranfering line break to {derge_hfml_path.stem}..')
    #     derge_hfml = derge_hfml_path.read_text(encoding='utf-8')
    #     pudrak_hfml = pudrak_hfml_path.read_text(encoding='utf-8')
    #     pudrak_hfml = preprocessing_pudrak(pudrak_hfml)
    #     derge_pudrak_hfml = transfer_pg_br(derge_hfml, pudrak_hfml)
    #     Path(f'./derge_pudrak/{pudrak_hfml_path.stem}.txt').write_text(derge_pudrak_hfml, encoding='utf-8')
    #     print(f'INFO: {pudrak_hfml_path.stem} completed..')
    
    # google_hfml_paths = list(Path('./pudrak_google').iterdir())
    # derge_hfml_paths = list(Path('./derge_vol').iterdir())
    # derge_hfml_paths.sort()
    # pudrak_hfml_paths = list(Path('./pudrak_trans').iterdir())
    # pudrak_hfml_paths.sort()
    # target_name = "derge"
    # pipeline(derge_hfml_paths, pudrak_hfml_paths, target_name)
    
    # hfml_paths = list(Path('./trans_derge').iterdir())
    # hfml_paths.sort()
    target_name = "trans"
    # for hfml_path in hfml_paths:
    hfml_path = Path(f'./{target_name}/v049.txt')
    hfml = hfml_path.read_text(encoding='utf-8')
    save_pagewise(hfml, hfml_path.stem, target_name)


