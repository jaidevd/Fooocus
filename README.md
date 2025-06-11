## Setup

```bash
$ pip install -r requirements_versions.txt
$ python entry_with_update.py --preset realistic
```

The last step here is only meant for downloading the models. This may take some
time. When it finishes, the gradio app will start. At this time, stop the script with `Ctrl+C`.

## Usage

**Warning**: Takes prohibitively long on CPU. Use a GPU for reasonable
performance.

Once the models are downloaded, use inpainting as follows:

1. Interactively generate a mask for a given image as follows:
  ```bash
  $ python masker.py ./path/to/input-image.png ./path/to/output-mask.png
  ```

2. Run the inpainting CLI as follows:

  ```bash
  $ python inpaint.py -i ./path/to/input.png --mask ./path/to/output-mask.png
  ```
The output will be saved in the `./outputs/` directory.

**Note**: On OSX, set the envvar `PYTORCH_ENABLE_MPS_FALLBACK=1`, although you
should not have to use this at all.

```bash
$ PYTORCH_ENABLE_MPS_FALLBACK=1 python inpaint.py -i ./path/to/input.png --mask ./path/to/output-mask.png
```
