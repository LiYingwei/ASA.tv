import os

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .settings import VIDEO_COVER_DIR


@login_required
def myupload(request):
    # assert 'op' in request.GET
    # assert 'ct' in request.GET
    # op = int(request.GET['op'])
    # ct = int(request.GET['ct'])
    # if ct > 20:
    #    ct = 20
    return JsonResponse(list(map(
        lambda video: {
            'rec': video.base.rec,
            'filename': video.base.filename,
            'playCount': video.play_count,
            'col': video.collection.name,
        },
        FileEXT.objects.filter(uploader=request.user).order_by('base__rec')
    )), safe=False)


class VideoCoverAJAX(View):

    def get(self, request, rec, *args, **kwargs):
        try:
            f = open(os.path.join(VIDEO_COVER_DIR, rec), "rb")
        except Exception:
            f = open(os.path.join(VIDEO_COVER_DIR, 'default'), "rb")
        return HttpResponse(f.read(), content_type='image')

    def post(self, request, rec, *args, **kwargs):
        try:
            video = File.objects.get(rec=int(rec))
        except Exception:
            return JsonResponse({
                'status': 'error',
                'reason': 'video file does not exists'
            })
        if video.ext.uploader == request.user:
            with open(os.path.join(VIDEO_COVER_DIR, rec), "wb") as f:
                f.write(request.body)
            return JsonResponse({
                'status': 'OK'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'reason': 'Permission Denied: you are not the uploader'
            })

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


video_cover_ajax = VideoCoverAJAX.as_view()


def getVideoToken(request, rec):
    try:
        file_ = File.objects.get(rec=rec)
    except Exception:
        return HttpResponse('', status=404)
    return JsonResponse({'token': file_.token}, status=201)


def search(request, filename):
    file_list = File.objects.filter(filename__contains=filename)
    if (getattr(settings, 'ASA_WITH_STRICT_VIDEO_AUTH', False) is True):
        file_list = file_list.exclude(ext__onshow=False)
    
    return JsonResponse(list(map(
        lambda __file: {
            'rec': __file.rec,
            'filename': __file.filename,
            'playCount': __file.ext.play_count,
            'col': __file.ext.collection.name,
        },
        file_list)), safe=False)
