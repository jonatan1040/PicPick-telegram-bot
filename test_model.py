from PIL import Image

import model


def test_paste_faces():
    pasted = model.paste_face("picture/obama.jpg", -378265149)
    Image.open(pasted).show()