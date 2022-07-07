IN_DIR   = ./images #FULL PATH
IMG_TYPE = jpg
all:
	python main.py --in_dir $(IN_DIR) --img_type $(IMG_TYPE)
