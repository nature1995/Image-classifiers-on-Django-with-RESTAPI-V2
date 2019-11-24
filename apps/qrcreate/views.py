from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from django.utils.six import BytesIO


@login_required(login_url='/accounts/login/')
def generate_qrcode(request, data):
    img = qrcode.make(data)

    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()

    response = HttpResponse(image_stream, content_type="image/png")
    return response

