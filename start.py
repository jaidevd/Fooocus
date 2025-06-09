import os
import yaml
from orderedattrdict import AttrDict


from modules.model_loader import load_file_from_url
from modules import config

with open('config.yaml', 'r') as fin:
    cfg = AttrDict(yaml.safe_load(fin))


vae_filenames = cfg['VAE_FILENAMES']
args = cfg['DEFAULT_ARGS']


os.environ["U2NET_HOME"] = config.path_inpaint

os.environ['GRADIO_TEMP_DIR'] = config.temp_path


def download_models(default_model, previous_default_models, checkpoint_downloads, embeddings_downloads, lora_downloads, vae_downloads):
    from modules.util import get_file_from_folder_list

    for file in vae_filenames:
        load_file_from_url(url=file['url'], model_dir=config.path_vae_approx, file_name=file['filename'])

    load_file_from_url(
        url='https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin',
        model_dir=config.path_fooocus_expansion,
        file_name='pytorch_model.bin'
    )

    if args.get('disable_preset_download', False):
        print('Skipped model download.')
        return default_model, checkpoint_downloads

    if not args.get('always_download_new_model', False):
        if not os.path.isfile(get_file_from_folder_list(default_model, config.paths_checkpoints)):
            for alternative_model_name in previous_default_models:
                if os.path.isfile(get_file_from_folder_list(alternative_model_name, config.paths_checkpoints)):
                    print(f'You do not have [{default_model}] but you have [{alternative_model_name}].')
                    print(f'Fooocus will use [{alternative_model_name}] to avoid downloading new models, '
                          f'but you are not using the latest models.')
                    print('Use --always-download-new-model to avoid fallback and always get new models.')
                    checkpoint_downloads = {}
                    default_model = alternative_model_name
                    break

    for file_name, url in checkpoint_downloads.items():
        model_dir = os.path.dirname(get_file_from_folder_list(file_name, config.paths_checkpoints))
        load_file_from_url(url=url, model_dir=model_dir, file_name=file_name)
    for file_name, url in embeddings_downloads.items():
        load_file_from_url(url=url, model_dir=config.path_embeddings, file_name=file_name)
    for file_name, url in lora_downloads.items():
        model_dir = os.path.dirname(get_file_from_folder_list(file_name, config.paths_loras))
        load_file_from_url(url=url, model_dir=model_dir, file_name=file_name)
    for file_name, url in vae_downloads.items():
        load_file_from_url(url=url, model_dir=config.path_vae, file_name=file_name)

    return default_model, checkpoint_downloads


config.default_base_model_name, config.checkpoint_downloads = download_models(
    config.default_base_model_name, config.previous_default_models, config.checkpoint_downloads,
    config.embeddings_downloads, config.lora_downloads, config.vae_downloads)

config.update_files()
print(args)

from webui import *
