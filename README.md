# *IDPL-PFOD: An Image Dataset of Printed Farsi Text for OCR Research*
This repository contains IDPL-PFOD that is an image dataset of printed Farsi text for Farsi optical character recognition researches.

Please refer to the following article(dataset's article), if you use dataset: 

F. S. Hosseini, S. Kashef, E. Shabaninia, and H. Nezamabadi-pour, "IDPL-PFOD: An Image Dataset of Printed Farsi Text for OCR Research, In Proceedings of " *The Second International Workshop on NLP Solutions for Under Resourced Languages(NSURL 2021) co-located with ICNLSP 2021, pages 22-31,Trento, Italy.* Association for Computational Linguistics.

You can download the dataset's article with the following links:

+ [2021NSURL-1.4](https://drive.google.com/file/d/1zqA70FpXBZt1HGLT0YUwBRQ3c_DBeNiV/view?usp=sharing)
+ [ACL Anthology website](https://aclanthology.org/2021.nsurl-1.4/)
+ [Google Scholar website](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=idpl-pfod&oq=i)

The full dataset is uploaded in Google Drive which can be downloaded with the following link:

 + [Google Drive](https://drive.google.com/drive/folders/1TaQ5gZ4Q3ROw_X_HQi_U8lFenrwVlzlT?usp=sharing)
 
**Notes:**
 + *IDPL stands for “Intelligent Data Processing Laboratory”.*

 + *PFOD stands for “Printed Farsi OCR Dataset”.*
 
 + *The size of the dataset is 507 MB.*

## IDPL-PFOD Description
IDPL-PFOD:
+ Is an artificial image dataset of printed Farsi text.

+ Has 30,138 images in **tif** format, and each image contains a line of real Farsi text.

+ The dimensions of the images are 700 x 50 pixels.

+ 50% of the images are generated with a plain white background, 40% with a noisy background and 10% with a texture background.
 
+ To increase the similarity of images with real images,some distortion and blur is added to 10% of the total images. More precisely, we have:
  + 4% sloping distortion,
  
  + 1% sinewave distortion,
 
  + 3% blur,
  
  + 2% both blur and one type of distortion.
  
+ To generate images, 11 common Farsi fonts with 2 font styles, 7 font sizes and 12 different patterns (for image with Texture background) have been used.

+ To record image information, we have created a CSV file that has 30,138 rows, each row corresponding to an image.
 
**Notes:**

 + *We used [MirasText](https://github.com/miras-tech/MirasText/tree/master/MirasText) Dataset to generate text of each image.*

 + *We generated IDPL-PFOD's images using Python programming language.*

 + *We used part of the code published [here](https://github.com/Belval/TextRecognitionDataGenerator) to add SineWave distortion to our images.*

## Synthetic data generation script

To help researchers recreate and extend the dataset, `generate_farsi_dataset.py`
provides a simple way to render Farsi text line images using any set of fonts
and optional background pictures.

### Usage

```bash
python generate_farsi_dataset.py \
    --font-dir path/to/fonts \
    --bg-dir path/to/backgrounds \
    --text-file path/to/farsi_lines.txt \
    --output-dir dataset
```

* `--font-dir` should contain TTF fonts and can include far more than the
  original 11 used for IDPL-PFOD.
* `--bg-dir` may contain any images to be resized and used as background
  textures in addition to the plain white and noisy options.
* `--text-file` is a UTF‑8 file with one line of Farsi text per row.

The script saves images and a `labels.csv` file describing font, size,
background type and applied effects.

## Summary of IDPL-PFOD
| | **Plain white** | **Noisy** | **Texture** | **Total images**| **Total Lines** | **Total Words** |
:-:|:-:|:-:|:-:|:-:|:-:|:-:
| **Each font** | 1,370 | 1,096 | 273 or 274 | 2,739 or 2,740 | 2,739 or 2,740 | 41,085 or 41,100 |
| **Total fonts** | 15,070 | 12,056 | 3,012 | 30,138 | 30,138 | 452,070 |

## Some of generated images in png format
#### *Plain white background:*
![](images/00001.png)
#### 
![](images/00002.png)
#### *Noisy background:*
![](images/00003.png)
#### 
![](images/00004.png)
#### 
![](images/00005.png)
#### *Texture background:*
![](images/00006.png)
#### 
![](images/00007.png)
#### 
![](images/00008.png)
