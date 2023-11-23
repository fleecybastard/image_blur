from ImageProccessor import ImageProcessor


def process():

    with open(f'test1.jpg', 'rb') as f:
        r = ImageProcessor.process_image(f.read(), blur=True)
        with open(f'result.jpg', 'wb') as wf:
            wf.write(r)


if __name__ == '__main__':
    process()
